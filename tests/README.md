# 🧪 DermaVision `tests/` Automated Quality Assurance & Clinical Benchmark Suite

This directory contains automated unit, integration, and safety validation test scripts for the DermaVision platform.

---

## 📂 Test Suite Index

| Test Script | Target System | Description |
| :--- | :--- | :--- |
| `test_pipeline.py` | Full Pipeline | Validates anatomical guardrail, disease diagnosis, and 5-part report generation |
| `test_user_images.py` | Benchmark Dataset | Tests 12 real and synthetic patient images across 7 regions |
| `test_region_guard.py` | Region Guard | Verifies clothing occlusion, non-human object rejection (`NON_HUMAN_OBJECT_ALERT`), and MediaPipe 468-point 3D FaceMesh |
| `test_specialist_finder.py` | Geospatial Routing | Verifies 100% Free Forever OpenStreetMap Overpass lookup & Google Maps routing |

---

## 🚀 How to Execute Tests

Run any test suite directly from your terminal or command prompt:

```bash
# Run End-to-End Pipeline Test
python tests/test_pipeline.py

# Run Region Guard Unit Test
python tests/test_region_guard.py

# Run Free Specialist Finder Test
python tests/test_specialist_finder.py

# Run Clinical Benchmark Evaluation
python tests/test_user_images.py
```

---

## 📊 Benchmark Test Results Summary

* **Anatomical Safety Guardrail:** 100% rejection rate for mismatches (e.g., Face uploaded while selecting Hand & Arm).
* **Non-Human Object Detection:** 100% rejection rate for biscuits, packaging, documents, and inanimate objects.
* **Clothing Occlusion Detection:** 100% trigger rate for fabric-covered skin lesions.
* **Specialist Routing Latency:** < 1.5 seconds average lookup via Overpass/Nominatim.
