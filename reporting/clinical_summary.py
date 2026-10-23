"""
ClinicalSummary: 5-Part Structured Dermatological Report Assembler
Structures patient reports according to clinical documentation best practices.
"""

from typing import Dict, Any

class ClinicalSummary:
    """
    Standardizes clinical report formatting across 5 key dimensions:
    1. Definition & Presentation
    2. Occurrence & Demographics
    3. Spreadability & Transmission
    4. Dietary Guidance
    5. Pharmacological & Lifestyle Protocol
    """

    @classmethod
    def assemble_report_text(
        cls,
        condition_name: str,
        region: str,
        confidence: float,
        sections: Dict[str, Any]
    ) -> str:
        """Assembles a clean, printable ASCII/UTF-8 clinical summary for patients."""
        header = f"""DERMAVISION CLINICAL DERMATOLOGY REPORT
============================================================
Target Anatomical Region: {region}
Condition Diagnosed:      {condition_name}
Diagnostic Confidence:    {confidence}%
Report Generation:        Autonomous Clinical AI Engine
============================================================
"""
        body_parts = []
        sec_keys = [
            ("1_definition", "1. DEFINITION & PATHOLOGY"),
            ("2_occurrence", "2. OCCURRENCE & DEMOGRAPHICS"),
            ("3_spreadability", "3. SPREADABILITY & TRANSMISSION"),
            ("4_dietary_protocol", "4. DIETARY PROTOCOL"),
            ("5_medicine_treatment", "5. MEDICINE & TREATMENT PROTOCOL")
        ]

        for key, title in sec_keys:
            data = sections.get(key, {})
            if key == "4_dietary_protocol":
                content = f"- Recommended: {data.get('intake_foods', 'N/A')}\n- Avoid: {data.get('avoid_foods', 'N/A')}"
            elif key == "5_medicine_treatment":
                content = f"{data.get('treatment_content', '')}\n\nWARNING:\n{data.get('doctor_alert', '')}"
            else:
                content = data.get("content", "")

            body_parts.append(f"\n{title}\n{'-' * len(title)}\n{content.strip()}\n")

        footer = """============================================================
NOTICE: This report is for educational decision support.
Consult a licensed dermatologist for official medical evaluation.
============================================================"""

        return header + "".join(body_parts) + footer
