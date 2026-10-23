"""
TextureAnalyzer: Dermatological Skin Lesion Texture & Micro-relief Analysis
Measures surface roughness, papular elevation, uniformity, and entropy.
"""

import cv2
import numpy as np
from typing import Dict, Any

class TextureAnalyzer:
    """
    Computes statistical and micro-relief surface descriptors of skin patches.
    Differentiates smooth healthy epidermis from scaly (psoriasiform),
    papular (acneiform), or verrucous textures.
    """

    @staticmethod
    def compute_local_variance(gray_image: np.ndarray, ksize: int = 7) -> float:
        """Computes mean local variance across the skin surface."""
        if len(gray_image.shape) == 3:
            gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
        mean = cv2.blur(gray_image.astype(np.float32), (ksize, ksize))
        sqr_mean = cv2.blur((gray_image.astype(np.float32)) ** 2, (ksize, ksize))
        variance = np.maximum(sqr_mean - mean ** 2, 0)
        return float(np.mean(variance))

    @staticmethod
    def compute_laplacian_sharpness(gray_image: np.ndarray) -> float:
        """Measures high-frequency gradient sharpness via Laplacian variance."""
        if len(gray_image.shape) == 3:
            gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray_image, cv2.CV_64F)
        return float(lap.var())

    @classmethod
    def analyze_skin_texture(cls, image_bgr: np.ndarray) -> Dict[str, Any]:
        """
        Extracts comprehensive clinical texture profile:
        - roughness_index: surface irregularity
        - sharpness: focus adequacy
        - homogeneity: smoothness score [0.0 - 1.0]
        - lesion_texture_type: classification tag
        """
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        variance = cls.compute_local_variance(gray)
        sharpness = cls.compute_laplacian_sharpness(gray)

        # Normalized homogeneity: higher for smooth healthy skin, lower for textured plaques
        homogeneity = float(1.0 / (1.0 + (variance / 100.0)))

        if variance < 80.0:
            texture_type = "SMOOTH_NORMAL_EPIDERMIS"
        elif variance < 250.0:
            texture_type = "MILD_MACULAR_IRREGULARITY"
        elif variance < 600.0:
            texture_type = "PAPULAR_ERYTHEMATOUS"
        else:
            texture_type = "SEVERE_PLAQUE_HYPERKERATOTIC"

        return {
            "local_variance": round(variance, 2),
            "sharpness": round(sharpness, 2),
            "homogeneity": round(homogeneity, 4),
            "texture_classification": texture_type,
            "is_sufficiently_focused": sharpness >= 30.0
        }
