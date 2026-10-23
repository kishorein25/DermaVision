"""
LandmarkGeometry: 3D Facial & Anatomical Landmark Vector Calculations
Computes spatial bounds, symmetry, tilt, and anatomical region coordinates.
"""

import math
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

class LandmarkGeometry:
    """
    Analyzes 468-point 3D facial mesh coordinates for anatomical boundaries,
    facial symmetry, head posture, and regional sub-zones (forehead, cheeks, chin).
    """

    # Key landmark indices in MediaPipe 468-point FaceMesh
    NOSE_TIP = 1
    CHIN = 152
    LEFT_EYE_OUTER = 33
    RIGHT_EYE_OUTER = 263
    FOREHEAD_TOP = 10
    LEFT_CHEEK = 234
    RIGHT_CHEEK = 454

    @classmethod
    def compute_bounding_box(cls, landmarks_xyz: List[Tuple[float, float, float]], img_w: int, img_h: int) -> Dict[str, int]:
        """Calculates pixel-space bounding box enclosing landmark points."""
        xs = [pt[0] * img_w for pt in landmarks_xyz]
        ys = [pt[1] * img_h for pt in landmarks_xyz]

        x_min = max(0, int(min(xs)))
        y_min = max(0, int(min(ys)))
        x_max = min(img_w, int(max(xs)))
        y_max = min(img_h, int(max(ys)))

        return {
            "x": x_min,
            "y": y_min,
            "w": x_max - x_min,
            "h": y_max - y_min,
            "area": (x_max - x_min) * (y_max - y_min)
        }

    @classmethod
    def compute_head_pose_angles(cls, landmarks_xyz: List[Tuple[float, float, float]]) -> Dict[str, float]:
        """
        Estimates yaw, pitch, and roll rotation angles from 3D facial vectors.
        Helps verify whether the patient's face is oriented within diagnostic limits.
        """
        if len(landmarks_xyz) < 468:
            return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}

        left_eye = np.array(landmarks_xyz[cls.LEFT_EYE_OUTER])
        right_eye = np.array(landmarks_xyz[cls.RIGHT_EYE_OUTER])
        nose = np.array(landmarks_xyz[cls.NOSE_TIP])
        chin = np.array(landmarks_xyz[cls.CHIN])

        # Roll: angle between eyes in xy plane
        d_eye = right_eye - left_eye
        roll_rad = math.atan2(d_eye[1], d_eye[0])
        roll_deg = math.degrees(roll_rad)

        # Yaw: horizontal offset of nose relative to eye center
        eye_center_x = (left_eye[0] + right_eye[0]) / 2.0
        eye_width = abs(right_eye[0] - left_eye[0]) or 1e-5
        yaw_ratio = (nose[0] - eye_center_x) / eye_width
        yaw_deg = yaw_ratio * 90.0

        # Pitch: vertical offset of nose relative to eye-chin line
        face_height = abs(chin[1] - landmarks_xyz[cls.FOREHEAD_TOP][1]) or 1e-5
        pitch_ratio = (nose[1] - landmarks_xyz[cls.FOREHEAD_TOP][1]) / face_height
        pitch_deg = (pitch_ratio - 0.5) * 60.0

        return {
            "yaw": round(yaw_deg, 2),
            "pitch": round(pitch_deg, 2),
            "roll": round(roll_deg, 2)
        }

    @classmethod
    def is_pose_acceptable_for_diagnosis(cls, angles: Dict[str, float], max_yaw: float = 40.0, max_pitch: float = 35.0) -> bool:
        """Determines if the head rotation is suitable for accurate clinical evaluation."""
        return abs(angles.get("yaw", 0)) <= max_yaw and abs(angles.get("pitch", 0)) <= max_pitch
