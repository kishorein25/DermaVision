# 🩺 DermaVision — `diagnose` Core Clinical Engine Subfolder

This directory contains the modular clinical, anatomical, diagnostic, evidence, reporting, and referral engines powering the DermaVision Dermatology AI platform.

---

## 📁 File Structure & Function Overview

```
diagnose/
├── __init__.py             # Package initializer exposing core engines
├── region_guard.py         # MediaPipe 468-point 3D anatomical verification & anti-hallucination guard
├── disease_engine.py       # Dual-vision diagnostic engine with Ollama Llama 3.2 vision
├── evidence_agent.py       # Autonomous clinical verification agent & 23-disease differential proof
├── specialist_finder.py    # 100% Free Forever OpenStreetMap & Google Maps clinic finder
├── report_generator.py     # 5-part structured clinical report generator
├── chat_assistant.py       # Interactive clinical Q&A conversational assistant
└── README.md               # This architectural reference documentation
```

---

## 🔬 Detailed Module Breakdown

### 1. `region_guard.py` — Anatomical Region Guard & Anti-Hallucination
- **Core Class:** `RegionGuard`
- **Key Functions:**
  - `verify_region(image, selected_region) -> Dict`: Performs deep anatomical verification against the selected user region.
  - `_detect_landmarks(image)`: Uses MediaPipe 468-point 3D FaceMesh + BlazeFace ($\ge 0.55$) for true facial geometry verification.
  - `_verify_clothing_occlusion(image)`: Color variance and texture check to detect clothing or fabric obstruction.
  - `_verify_non_human(image)`: Rejects non-biological artifacts, wrappers, biscuits, and inanimate objects with `NON_HUMAN_OBJECT_ALERT`.
- **Supported Anatomical Regions (7):**
  1. Face & Neck
  2. Chest & Abdomen
  3. Back & Spine
  4. Arms & Forearms
  5. Hands, Palms & Nails
  6. Legs & Thighs
  7. Feet, Soles & Toenails

---

### 2. `disease_engine.py` — Dual-Vision Clinical Diagnostic Engine
- **Core Class:** `DiseaseEngine`
- **Key Functions:**
  - `analyze_skin(image, verified_region) -> Dict`: Diagnoses primary skin condition across 23 standardized clinical conditions per region.
  - Handles **Facial Tattoos / Microblading** vs dermatological lesions.
  - Evaluates **Normal / Healthy Skin** with 0% unwarranted pathology triggers.
  - Multi-condition detection for co-occurring lesions (e.g., Acne Vulgaris + Post-Inflammatory Hyperpigmentation).

---

### 3. `evidence_agent.py` — Autonomous Clinical Evidence & Verification Agent
- **Core Class:** `ClinicalEvidenceAgent`
- **Key Functions:**
  - `gather_evidence(condition_name, region, confidence, image_features) -> Dict`: Generates differential elimination tables and clinical justifications.
  - Evaluates all **23 candidate conditions** per region with live search links to scientific archives (PubMed, DermNet NZ, British Journal of Dermatology).
  - Produces structured rule-out proofs for alternative candidates.

---

### 4. `specialist_finder.py` — 100% Free Forever Map & Clinic Referral
- **Core Class:** `SpecialistFinder`
- **Key Functions:**
  - `detect_user_location() -> (city, lat, lon)`: Automatically detects user city and GPS coordinates using network IP geolocation (Zero API keys, zero permissions required).
  - `find_specialists(location, lat, lon) -> Dict`: Finds real surrounding dermatologists, clinics, and hospitals using the OpenStreetMap (OSM) Overpass API and Nominatim geocoding.
  - Generates direct Google Maps turn-by-turn navigation URLs (`https://www.google.com/maps/dir/?api=1&destination={lat},{lon}`) and location search queries (`dermatologists near me`).
  - **100% Free Forever:** Zero billing, zero credit cards, and zero paid API keys needed.

---

### 5. `report_generator.py` — 5-Part Clinical Report Generator
- **Core Class:** `ClinicalReportGenerator`
- **Key Functions:**
  - `generate_report(condition_data, region) -> Dict`: Produces structured 5-part patient-facing dermatological documentation:
    1. **Definition & Clinical Presentation**
    2. **Occurrence & Prevalence**
    3. **Spreadability & Contagion Assessment**
    4. **Dietary Protocol (Beneficial Foods vs Harmful Foods to Avoid)**
    5. **Medicine & Clinical Treatment Protocol (with mandatory Physician Alert)**

---

### 6. `chat_assistant.py` — Interactive Patient Q&A Bot
- **Core Class:** `DermaChatAssistant`
- **Key Functions:**
  - `answer_question(question, context, history) -> str`: Real-time interactive patient Q&A powered by local Ollama Llama 3.2, grounding responses in the active clinical diagnosis and region.

---

## 🚀 How to Import & Use

```python
from diagnose import (
    RegionGuard,
    DiseaseEngine,
    ClinicalEvidenceAgent,
    SpecialistFinder,
    ClinicalReportGenerator,
    DermaChatAssistant
)

# 1. Verify anatomical region
guard = RegionGuard()
verification = guard.verify_region(image_cv2, "Face & Neck")

# 2. Diagnose if valid
if verification["valid"]:
    engine = DiseaseEngine()
    diagnosis = engine.analyze_skin(image_pil, "Face & Neck")

    # 3. Find real surrounding dermatologists (100% Free Forever)
    finder = SpecialistFinder()
    loc, lat, lon = finder.detect_user_location()
    specialists = finder.find_specialists(location=loc, lat=lat, lon=lon)
```
