"""
ColorSegmentation: Skin Lesion Chromatic & Pigmentation Analysis
Calculates Erythema Index (EI), Melanin Index (MI), and CIELAB color shifts.
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple

class ColorSegmentation:
    """
    Analyzes color distributions, vascular redness (erythema),
    hyperpigmentation/melanin density, and skin undertones.
    """

    @staticmethod
    def extract_skin_mask(image_bgr: np.ndarray) -> np.ndarray:
        """
        Segments biological skin pixels using adaptive YCrCb and HSV thresholding.
        Filters out dark background or neutral clinic paper.
        """
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)

        # Typical human skin bounds across all Fitzpatrick phototypes I-VI
        lower_hsv = np.array([0, 15, 30], dtype=np.uint8)
        upper_hsv = np.array([45, 255, 255], dtype=np.uint8)
        mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

        lower_ycrcb = np.array([0, 130, 77], dtype=np.uint8)
        upper_ycrcb = np.array([255, 177, 127], dtype=np.uint8)
        mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

        skin_mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        return skin_mask

    @classmethod
    def calculate_erythema_and_melanin_index(cls, image_bgr: np.ndarray) -> Dict[str, float]:
        """
        Calculates standard optical indices:
        - Erythema Index (EI): log(R_refl) - log(G_refl)
        - Melanin Index (MI): log(1 / R_refl)
        """
        b, g, r = cv2.split(image_bgr.astype(np.float32) + 1.0)  # Avoid zero division
        r_norm = r / 255.0
        g_norm = g / 255.0

        # Optical reflectance logarithm formulations
        ei_map = 100.0 * (np.log10(1.0 / np.maximum(g_norm, 1e-4)) - np.log10(1.0 / np.maximum(r_norm, 1e-4)))
        mi_map = 100.0 * np.log10(1.0 / np.maximum(r_norm, 1e-4))

        mean_ei = float(np.mean(ei_map))
        mean_mi = float(np.mean(mi_map))

        return {
            "erythema_index": round(mean_ei, 2),
            "melanin_index": round(mean_mi, 2),
            "is_erythematous": mean_ei > 12.0
        }
