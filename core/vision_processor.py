"""
VisionProcessor: Advanced Preprocessing, Illumination Correction & Normalization
Prepares clinical dermatological imagery for deep vision models and landmark detectors.
"""

import cv2
import numpy as np
from typing import Tuple, Optional
from PIL import Image

class VisionProcessor:
    """
    Standardizes input clinical dermatological imagery.
    Performs illumination balancing, noise filtering, and color space transformations.
    """

    @staticmethod
    def pil_to_cv2(image: Image.Image) -> np.ndarray:
        """Converts PIL RGB Image to OpenCV BGR ndarray."""
        rgb = np.array(image.convert("RGB"))
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(image: np.ndarray) -> Image.Image:
        """Converts OpenCV BGR ndarray to PIL RGB Image."""
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    @staticmethod
    def apply_clahe(image_bgr: np.ndarray, clip_limit: float = 2.0, tile_grid: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) on L-channel in LAB space.
        Normalizes varying clinic lighting conditions without over-saturating skin tones.
        """
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl, a, b))
        return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    @staticmethod
    def denoise_bilateral(image_bgr: np.ndarray, d: int = 9, sigma_color: float = 75, sigma_space: float = 75) -> np.ndarray:
        """
        Applies bilateral filtering to smooth high-frequency sensor noise
        while preserving crucial lesion edges and erythema boundaries.
        """
        return cv2.bilateralFilter(image_bgr, d, sigma_color, sigma_space)

    @classmethod
    def preprocess_clinical_image(cls, image_bgr: np.ndarray, target_max_dim: int = 1200) -> Tuple[np.ndarray, float]:
        """
        Complete standardized clinical preprocessing pipeline:
        1. Dimension scaling maintaining aspect ratio
        2. Bilateral edge-preserving noise suppression
        3. Adaptive illumination normalization
        """
        h, w = image_bgr.shape[:2]
        scale = 1.0
        if max(h, w) > target_max_dim:
            scale = target_max_dim / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            resized = cv2.resize(image_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
        else:
            resized = image_bgr.copy()

        denoised = cls.denoise_bilateral(resized, d=5, sigma_color=50, sigma_space=50)
        corrected = cls.apply_clahe(denoised, clip_limit=1.8)
        return corrected, scale
