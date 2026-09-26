import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

mp_face = mp.solutions.face_detection
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

REGIONS = ["face", "leg", "hand", "foot", "scalp", "back", "whole_body"]

_face_det = None
_hands_det = None
_pose_det = None


def _get_face_det():
    global _face_det
    if _face_det is None:
        _face_det = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)
    return _face_det


def _get_hands_det():
    global _hands_det
    if _hands_det is None:
        _hands_det = mp_hands.Hands(static_image_mode=True, max_num_hands=2,
                                    min_detection_confidence=0.5)
    return _hands_det


def _get_pose_det():
    global _pose_det
    if _pose_det is None:
        _pose_det = mp_pose.Pose(static_image_mode=True,
                                 model_complexity=1,
                                 min_detection_confidence=0.5)
    return _pose_det


def _pil_to_cv2(img):
    if isinstance(img, Image.Image):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return img


def detect_face(img):
    cv_img = _pil_to_cv2(img)
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    results = _get_face_det().process(rgb)
    return results.detections is not None and len(results.detections) > 0


def detect_hands(img):
    cv_img = _pil_to_cv2(img)
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    results = _get_hands_det().process(rgb)
    return results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks) > 0


def detect_pose(img):
    cv_img = _pil_to_cv2(img)
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    results = _get_pose_det().process(rgb)
    return results.pose_landmarks is not None


def _pose_landmarks(img):
    cv_img = _pil_to_cv2(img)
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    results = _get_pose_det().process(rgb)
    if results.pose_landmarks is None:
        return None
    return results.pose_landmarks.landmark


def get_detected_regions(img):
    found = []
    if detect_face(img):
        found.append("face")
    if detect_hands(img):
        found.append("hand")
    lm = _pose_landmarks(img)
    if lm is not None:
        found.append("body")
        h, w = img.size if isinstance(img, Image.Image) else img.shape[:2]
        vis = [l.visibility for l in lm]
        avg_vis = float(np.mean(vis))
        if avg_vis < 0.5:
            pass
        found.append("whole_body" if avg_vis > 0.6 else "body")
    return found


def validate_region(img, selected_region):
    if isinstance(img, Image.Image):
        w, h = img.size
    else:
        h, w = img.shape[:2]

    selected = selected_region.lower().strip()
    if selected not in REGIONS:
        return False, "Unknown region selected"

    face_found = detect_face(img)
    hand_found = detect_hands(img)
    lm = _pose_landmarks(img)

    if lm is not None:
        vis = [l.visibility for l in lm]
        avg_vis = float(np.mean(vis))

    # face region checks
    if selected == "face":
        if face_found:
            return True, "Face detected in image"
        if hand_found:
            return False, "This image contains a HAND, not a face. Please upload a face image."
        if lm is not None:
            return False, "This image contains a full body / other body part, not a face. Please upload a face image."
        return False, "No face detected in this image. Please upload a clear face image."

    # hand region checks
    if selected == "hand":
        if hand_found:
            return True, "Hand detected in image"
        if face_found:
            return False, "This image contains a FACE, not a hand. Please upload a hand image."
        if lm is not None:
            return False, "This image contains a body / other body part, not a hand. Please upload a hand image."
        return False, "No hand detected in this image. Please upload a clear hand image."

    # scalp region checks
    if selected == "scalp":
        if face_found and lm is not None:
            return True, "Scalp region detected (face + upper body area)"
        if face_found:
            return True, "Face with scalp/hair area detected above"
        if hand_found:
            return False, "This image contains a HAND, not a scalp. Please upload a scalp image."
        return False, "No scalp region detected. Please upload a clear scalp/hair image."

    # leg region checks
    if selected == "leg":
        if lm is not None and not face_found and not hand_found:
            return True, "Leg region detected (lower body limbs)"
        if lm is not None and face_found:
            return False, "This image contains a FACE. Please upload only the leg region."
        if face_found and not lm:
            return False, "This image contains a FACE, not a leg. Please upload a leg image."
        if hand_found:
            return False, "This image contains a HAND, not a leg. Please upload a leg image."
        if lm is not None:
            return True, "Body (leg area) detected in image"
        return False, "No leg region detected. Please upload a clear leg image."

    # foot region checks
    if selected == "foot":
        if lm is not None and not face_found:
            return True, "Foot/lower limb region detected"
        if face_found:
            return False, "This image contains a FACE, not a foot. Please upload a foot image."
        if hand_found:
            return False, "This image contains a HAND, not a foot. Please upload a foot image."
        if lm is not None and face_found:
            return False, "This image contains a face area. Please upload only the foot."
        return False, "No foot region detected. Please upload a clear foot image."

    # back region checks
    if selected == "back":
        if lm is not None and not face_found and not hand_found:
            return True, "Back region detected (torso without face/limbs)"
        if face_found:
            return False, "This image contains a FACE. Please upload a back image."
        if hand_found:
            return False, "This image contains a HAND, not a back. Please upload a back image."
        return False, "No back region detected. Please upload a clear back image."

    # whole body checks
    if selected == "whole_body":
        if lm is not None:
            return True, "Full body detected in image"
        if face_found and hand_found:
            return True, "Face and hand detected - acceptable as body regions"
        if face_found:
            return False, "Only a FACE detected. Please upload a full body image."
        if hand_found:
            return False, "Only a HAND detected. Please upload a full body image."
        return False, "No body detected in this image. Please upload a full body image."

    return False, "Region validation failed"


def detect_region_type(img):
    """Auto-detect what region the uploaded image contains."""
    face_found = detect_face(img)
    hand_found = detect_hands(img)
    lm = _pose_landmarks(img)

    if face_found:
        if hand_found:
            return "face_hand"
        return "face"
    if hand_found:
        return "hand"
    if lm is not None:
        return "body"
    return "unknown"


def is_normal_skin(confidence):
    """If confidence is below threshold, consider it healthy/normal skin."""
    return confidence < 0.35