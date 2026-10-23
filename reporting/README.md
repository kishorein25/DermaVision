# 📑 DermaVision `reporting/` Clinical Documentation Engine

This package manages the generation of structured 5-part clinical reports, patient dietary protocols, pharmacological advisory notes, and compliant medical disclaimers.

---

## 📂 Architecture

```
reporting/
├── __init__.py               # Package exposure
├── clinical_summary.py       # 5-section medical report assembler & text formatter
├── dietary_guidelines.py     # Nutritional mapping: anti-inflammatory vs inflammatory triggers
├── treatment_protocols.py    # Topical, systemic & barrier repair recommendations
├── disclaimer_engine.py      # Standardized clinical disclaimers & HTML banners
└── README.md                 # Reporting system documentation
```

---

## 📋 The 5-Part Clinical Report Standard

Every generated patient summary adheres to the following structured format:

1. **Definition & Presentation**: Clinical pathology, cell biology, and hallmark morphology.
2. **Occurrence & Demographics**: Epidemiology, age distribution, and environmental triggers.
3. **Spreadability & Transmission**: Contagion analysis, autoinoculation risks, and contact guidance.
4. **Dietary Protocol**: Evidence-based foods to consume vs high-glycemic/histaminic foods to avoid.
5. **Medicine & Treatment**: First-line topical management with explicit physician safety warnings.
