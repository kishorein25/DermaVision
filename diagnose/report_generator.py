# ==============================================================================
# DermaVision: Stage 4 - 5-Part Clinical Report Generator
# Powered by Local Ollama (llama3.2:1b) + Medical Knowledge Base (config.py)
# ==============================================================================

import requests
import json
from typing import Dict, Any, Optional
import config

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

class ClinicalReportGenerator:
    def __init__(self, model_name: str = MODEL_NAME, api_url: str = OLLAMA_API_URL):
        self.model_name = model_name
        self.api_url = api_url
        self._check_ollama_available()

    def _check_ollama_available(self) -> bool:
        """Pings Ollama local service to verify connection."""
        try:
            res = requests.get("http://localhost:11434/api/tags", timeout=2.0)
            if res.status_code == 200:
                return True
        except Exception:
            pass
        return False

    def generate_report(self, diagnosis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates the 5-Part Structured Clinical Report:
        1. Definition of this disease
        2. Occurrence (How commonly it occurs)
        3. Spreadability (Is it contagious or not)
        4. Dietary Protocol (Foods to intake vs. Foods to avoid)
        5. Medicine & Treatment Suggestions (with prominent Doctor Alert)
        """
        condition = diagnosis_result.get("condition", {})
        region = diagnosis_result.get("region", "Face")
        confidence = diagnosis_result.get("confidence", 95.0)
        c_name = condition.get("name", "Unknown Condition")
        c_category = condition.get("category", "disease")
        empathetic_msg = condition.get("empathetic_message", "Take gentle care of your skin.")
        is_contagious = condition.get("is_contagious", False)

        # Baseline structured data from clinical database (guaranteed fallback)
        definition_text = condition.get("definition", "Dermatological presentation affecting the cutaneous barrier.")
        occurrence_text = condition.get("occurrence", "Observed across various demographic groups.")
        spreadability_text = (
            "🚨 **CONTAGIOUS:** This condition can spread to other areas or individuals through direct contact or shared items."
            if is_contagious else
            "✅ **NON-CONTAGIOUS:** This condition is internal/inflammatory/benign and CANNOT spread to other people."
        )
        food_intake = condition.get("dietary_intake", "Antioxidant-rich foods, leafy greens, water (2-3L/day).")
        food_avoid = condition.get("dietary_avoid", "Processed sugars, high-glycemic snacks, alcohol.")
        treatment_text = condition.get("standard_treatment", "Gentle skin hygiene, non-comedogenic moisturizers, daily SPF 50 sunscreen.")

        # Attempt enrichment via local Ollama llama3.2:1b
        enriched_summary = None
        try:
            prompt = f"""You are a specialized clinical dermatology AI assistant.
Create a structured 5-part clinical report for:
Condition: {c_name}
Anatomical Region: {region}
Confidence: {confidence}%
Category: {c_category}

Provide clear, professional, empathetic guidance adhering to this exact format:
1. Definition: Concise clinical & plain English explanation.
2. Occurrence: Prevalence, who gets it, triggers.
3. Spreadability: Whether it is contagious or non-contagious.
4. Food Process: Recommended beneficial foods to intake AND harmful foods to strictly avoid.
5. Medicine Suggestions: Standard clinical / OTC topical solutions, followed by an alert to consult a doctor.

Keep the response concise, compassionate, and medically sound."""

            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "max_tokens": 500
                }
            }
            res = requests.post(self.api_url, json=payload, timeout=8.0)
            if res.status_code == 200:
                data = res.json()
                enriched_summary = data.get("response", "").strip()
        except Exception as e:
            # Graceful fallback: local knowledge base in config.py is already medically rich
            pass

        # Package the structured 5-part report
        report = {
            "condition_name": c_name,
            "region": region,
            "confidence": confidence,
            "category": c_category,
            "empathetic_banner": empathetic_msg,
            "sections": {
                "1_definition": {
                    "title": "1. Definition of Condition",
                    "icon": "📖",
                    "content": definition_text
                },
                "2_occurrence": {
                    "title": "2. Occurrence & Demographics",
                    "icon": "📊",
                    "content": occurrence_text
                },
                "3_spreadability": {
                    "title": "3. Spreadability / Contagion Status",
                    "icon": "🔄",
                    "is_contagious": is_contagious,
                    "content": spreadability_text
                },
                "4_dietary_protocol": {
                    "title": "4. Dietary Process (Intake & Avoidance)",
                    "icon": "🥗",
                    "intake_foods": food_intake,
                    "avoid_foods": food_avoid
                },
                "5_medicine_treatment": {
                    "title": "5. Medicine & Treatment Suggestions",
                    "icon": "💊",
                    "treatment_content": treatment_text,
                    "doctor_alert": (
                        "⚠️ **MANDATORY MEDICAL CONSULTATION ALERT:**\n\n"
                        "This report is generated for educational and preliminary screening purposes. "
                        "Prescription medications, steroids, oral antibiotics, and systemic drugs must "
                        "**ONLY be initiated under the direct clinical supervision of a licensed dermatologist or physician**."
                    )
                }
            },
            "llm_enrichment": enriched_summary,
            "engine": f"Meta Llama 3.2 (1B) + DermaVision Medical Database"
        }

        return report


if __name__ == "__main__":
    generator = ClinicalReportGenerator()
    dummy_diagnosis = {
        "condition": config.CONDITIONS_DB["Face"][5],  # Acne Vulgaris
        "region": "Face",
        "confidence": 96.5
    }
    rep = generator.generate_report(dummy_diagnosis)
    print("ClinicalReportGenerator successfully created report for:", rep["condition_name"])
    print("Report sections generated:", list(rep["sections"].keys()))

