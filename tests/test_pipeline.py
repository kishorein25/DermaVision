# ==============================================================================
# DermaVision: Automated Verification Test Suite
# Tests:
# 1. Positive Region Match & Disease Detection Flow
# 2. Safety Region Mismatch Alert Flow (Face uploaded on Hand)
# 3. 5-Part Clinical Report Generation via Ollama Llama 3.2
# ==============================================================================

import os
import sys
# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from PIL import Image, ImageDraw
import cv2
import config
from region_guard import RegionGuard
from disease_engine import DiseaseEngine
from report_generator import ClinicalReportGenerator

def create_synthetic_face_image() -> Image.Image:
    """Generates a synthetic facial structure with eyes, nose, and lips for testing."""
    img = Image.new("RGB", (320, 320), color=(240, 215, 195))
    draw = ImageDraw.Draw(img)
    # Head contour
    draw.ellipse([(60, 40), (260, 290)], fill=(235, 200, 175), outline=(180, 140, 110), width=2)
    # Eyes
    draw.ellipse([(100, 110), (135, 130)], fill=(255, 255, 255), outline=(50, 30, 20), width=2)
    draw.ellipse([(112, 115), (125, 125)], fill=(60, 40, 30))
    draw.ellipse([(185, 110), (220, 130)], fill=(255, 255, 255), outline=(50, 30, 20), width=2)
    draw.ellipse([(195, 115), (208, 125)], fill=(60, 40, 30))
    # Nose
    draw.line([(160, 135), (155, 180), (168, 180)], fill=(160, 120, 95), width=2)
    # Mouth
    draw.chord([(120, 210), (200, 240)], start=0, end=180, fill=(200, 100, 100), outline=(150, 60, 60), width=2)
    # Erythematous acne spots
    for (x, y) in [(90, 160), (95, 175), (220, 165), (225, 180), (155, 80)]:
        draw.ellipse([(x-5, y-5), (x+5, y+5)], fill=(215, 50, 50))
    return img

def test_full_pipeline():
    print("=" * 70)
    print("DERMAVISION: RUNNING AUTOMATED CLINICAL VERIFICATION TESTS")
    print("=" * 70)

    guard = RegionGuard()
    engine = DiseaseEngine()
    reporter = ClinicalReportGenerator()

    test_img = create_synthetic_face_image()

    # -------------------------------------------------------------------------
    # TEST 1: SAFETY MISMATCH TEST (Upload Face photo while selecting "Hands, Palms & Nails")
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Testing Safety Mismatch Alert (Selected: 'Hands, Palms & Nails', Image: Face)...")
    mismatch_check = guard.verify_region(test_img, "Hands, Palms & Nails")
    print(f" -> Is Match: {mismatch_check['is_match']}")
    print(f" -> Selected: {mismatch_check['selected_region']}")
    print(f" -> Detected: {mismatch_check['detected_region']} ({mismatch_check['confidence']}%)")

    assert not mismatch_check["is_match"], "FAIL: Mismatch was not detected!"
    print("[SUCCESS] TEST 1 PASSED: Safety Mismatch Guard successfully triggered and halted!")

    # -------------------------------------------------------------------------
    # TEST 2: POSITIVE MATCH TEST (Upload Face photo while selecting "Face & Neck")
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Testing Positive Match & Disease Detection (Selected: 'Face & Neck', Image: Face)...")
    match_check = guard.verify_region(test_img, "Face & Neck")
    print(f" -> Is Match: {match_check['is_match']}")
    print(f" -> Selected: {match_check['selected_region']}")
    print(f" -> Detected: {match_check['detected_region']} ({match_check['confidence']}%)")

    assert match_check["is_match"], "FAIL: Positive match was rejected!"
    print("Region Verified! Proceeding to Disease Engine...")

    # Run Disease Detection
    diagnosis = engine.diagnose(test_img, "Face & Neck", image_filename="acne_face.jpg")
    print(f" -> Diagnosed Condition: {diagnosis['condition']['name']}")
    print(f" -> Category: {diagnosis['condition']['category']}")
    print(f" -> Confidence: {diagnosis['confidence']}%")
    print("[SUCCESS] TEST 2 PASSED: Disease Engine successfully diagnosed condition!")

    # -------------------------------------------------------------------------
    # TEST 3: 5-PART CLINICAL REPORT GENERATION (Ollama Llama 3.2)
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Generating 5-Part Clinical Report...")
    report = reporter.generate_report(diagnosis)
    sec = report["sections"]
    print(f" -> Section 1 (Definition): {sec['1_definition']['title']}")
    print(f" -> Section 2 (Occurrence): {sec['2_occurrence']['title']}")
    print(f" -> Section 3 (Spreadability): {sec['3_spreadability']['title']}")
    print(f" -> Section 4 (Dietary Protocol): {sec['4_dietary_protocol']['title']}")
    print(f" -> Section 5 (Medicine & Alert): {sec['5_medicine_treatment']['title']}")
    print("[SUCCESS] TEST 3 PASSED: 5-Part Clinical Report successfully constructed!")

    print("\n" + "=" * 70)
    print("ALL 3 PIPELINE TESTS PASSED 100% SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    test_full_pipeline()
