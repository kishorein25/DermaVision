# ==============================================================================
# DermaVision: Unit Tests for RegionGuard & Anti-Hallucination Guardrail
# ==============================================================================

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from PIL import Image, ImageDraw
from region_guard import RegionGuard

def test_clothing_occlusion_detection():
    print("[TEST] Testing Clothing Occlusion Detection...")
    guard = RegionGuard()
    # Create synthetic solid checkered shirt fabric pattern
    fabric = np.zeros((400, 400, 3), dtype=np.uint8)
    fabric[::20, :] = [200, 30, 30]
    fabric[:, ::20] = [30, 30, 200]
    img = Image.fromarray(fabric)

    res = guard.verify_region(img, "Chest & Abdomen")
    print(f" -> Result for fabric: {res.get('alert_type', 'None')}")
    # Either clothing or mismatch detected, must not pass as clean skin
    assert not res["is_match"], "FAIL: Checkered fabric passed as verified skin!"
    print("[PASSED] Clothing/non-skin pattern successfully rejected.")

def test_non_human_object_rejection():
    print("[TEST] Testing Inanimate/Non-Human Object Rejection...")
    guard = RegionGuard()
    # Create pure high-contrast synthetic barcode / food packaging
    packaging = np.zeros((300, 300, 3), dtype=np.uint8)
    packaging[:, :100] = [255, 255, 0]  # Bright yellow
    packaging[:, 100:200] = [0, 0, 255] # Bright red
    packaging[:, 200:] = [0, 255, 0]    # Bright green
    img = Image.fromarray(packaging)

    res = guard.verify_region(img, "Face & Neck")
    assert not res["is_match"], "FAIL: Bright packaging passed as human face!"
    print(f"[PASSED] Inanimate packaging rejected with alert: {res.get('alert_type')}")

if __name__ == "__main__":
    test_clothing_occlusion_detection()
    test_non_human_object_rejection()
    print("\nALL REGION GUARD UNIT TESTS PASSED SUCCESSFULLY!")
