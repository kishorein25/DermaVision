# 🤖 DermaVision `agents/` Autonomous Verification System

This package implements the multi-agent cognitive architecture responsible for differential diagnosis elimination, autonomous clinical web search, and evidence evaluation.

---

## 📂 Architecture & Agents

```
agents/
├── __init__.py               # Agent package export
├── clinical_reasoner.py      # Probabilistic differential ranking & alternative rule-out
├── medical_search.py         # Autonomous PubMed, DermNet NZ & Scholar cross-referencing
├── evidence_evaluator.py     # Concordance thresholds, safety gating & normal tissue clearing
└── README.md                 # Agent architectural specification
```

---

## 🧠 Diagnostic Reasoning Workflow

```
[Vision Model Detection] 
         │
         ▼
[ClinicalReasoner] ────▶ Evaluates 23 standardized candidates per anatomical zone
         │
         ▼
[MedicalSearchAgent] ──▶ Generates direct PubMed / DermNet verification queries
         │
         ▼
[EvidenceEvaluator] ───▶ Gating: Confidence >= 80% (High), < 60% (Inconclusive)
         │
         ▼
[Structured Evidence Audit Table]
```
