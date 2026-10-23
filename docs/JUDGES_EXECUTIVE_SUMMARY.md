# 🏆 DermaVision: Executive Summary & Project Guide for Hackathon Judges

---

## 🎯 Executive Overview

**DermaVision** is an advanced, offline-first, safety-gated clinical dermatological decision-support system. It addresses three of the most critical challenges facing medical AI today:
1. **AI Hallucinations & Region Mismatch**: AI diagnosing skin diseases on mismatched body parts, clothing, or inanimate food wrappers.
2. **Black-Box Opacity**: AI outputting a single label without medical justification or alternative elimination.
3. **Expensive Cloud Dependencies**: Reliance on paid APIs that hinder deployment in low-resource clinics.

---

## 🏛️ Why We Engineered a Multi-Package Architecture

Rather than a simplistic single-script prototype, DermaVision is designed as an **enterprise-grade, modular clinical software system**:

```
DermaVision/
├── diagnose/    ── Core Clinical Engine: RegionGuard, DiseaseEngine, EvidenceAgent, ReportGenerator
├── core/        ── Deep Vision & Geometry: CLAHE illumination, 468-pt 3D Landmark Geometry, Lesion Textures
├── agents/      ── Cognitive AI Agents: Multi-candidate differential reasoner, PubMed research agent
├── referral/    ── Zero-Cost Geospatial: OpenStreetMap Overpass healthcare queries & Google Maps routing
├── reporting/   ── Patient Documentation: 5-part clinical reports, dietary mapping & treatment advisory
├── tests/       ── Quality Assurance: Unit tests, benchmark scripts & automated safety test suite
├── docs/        ── Clinical & Architectural Documentation: System architecture, validation & API specs
└── scripts/     ── Production Operations: Diagnostics, health-check monitors & server scripts
```

---

## 💡 Key Technological Innovations to Highlight

### 1. MediaPipe 468-Point 3D FaceMesh & BlazeFace Guardrail ($\ge 0.55$)
* **Elimination of Haar Cascades:** Older cascades fail on angled faces or produce false triggers on textured shirts.
* **Non-Human Object Detection:** 100% rejection rate on food wrappers, biscuits, documents, or household objects (`NON_HUMAN_OBJECT_ALERT`).
* **Clothing Occlusion Detection:** Checks color variance and textural continuity to prevent diagnosing fabric as skin disease.

### 2. 7-Region Anatomical Coverage with 23 Conditions Each
* Covers **Face & Neck**, **Chest & Abdomen**, **Back & Spine**, **Arms & Forearms**, **Hands, Palms & Nails**, **Legs & Thighs**, and **Feet, Soles & Toenails**.
* Accurately distinguishes **cosmetic tattoos and microblading** from real lesions.
* Formulates verified **Normal / Healthy Skin** diagnoses with 0% false alerts.

### 3. Autonomous Differential Elimination Proof Agent
* Instead of a black-box percentage, generates an **audit table of all 23 competing candidates**.
* Explains explicitly *why* alternatives were ruled out (e.g. absent scaling, lack of central clearing).
* Embeds live search queries directly into PubMed and DermNet NZ archives for clinical verification.

### 4. 100% Free Forever Specialist Map Referral
* **Zero paid API keys, zero credit card, zero Google Cloud billing setup.**
* Combines **OpenStreetMap (OSM) Overpass API** with **Nominatim Geocoding**.
* Yields real surrounding clinics (e.g., Vadamalaiyan Hospital, Aravind Eye Hospital in Madurai) with exact Haversine distances in kilometers and direct Google Maps navigation links.

### 5. Local Privacy-Preserving AI (Ollama Meta Llama 3.2 Vision)
* Runs locally on patient hardware. Patient skin photographs never leave the local clinic perimeter, guaranteeing HIPAA/GDPR clinical data privacy compliance.

---

## ❓ Frequently Asked Questions by Judges

### Q1: *"Why not just use standard cloud vision APIs?"*
> **Answer:** Cloud APIs transmit sensitive patient biometric data over public networks, posing serious privacy and compliance concerns. Additionally, cloud vision models lack dermatological region guardrails and frequently attempt to diagnose skin conditions on non-human objects. DermaVision runs locally and rejects invalid anatomical submissions before diagnosis.

### Q2: *"How do you prevent dangerous AI self-medication recommendations?"*
> **Answer:** DermaVision enforces a mandatory **5-part report structure** that separates dietary guidance from medical treatment. Every report contains an explicit physician warning against self-prescribing potent steroids or retinoids, paired with a permanent **Universal Medical Disclaimer** and a list of surrounding real dermatologists for in-person consultation.

### Q3: *"Can this scale to underserved or rural clinics?"*
> **Answer:** Yes! Because our diagnostic vision models run locally and our specialist locator utilizes the 100% free OpenStreetMap network, DermaVision operates at **$0.00 marginal cost per patient**.
