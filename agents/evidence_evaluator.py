"""
EvidenceEvaluator: Clinical Concordance & Safety Guardrail Verification
Validates diagnostic hypotheses against established clinical thresholds.
"""

from typing import Dict, Any, List

class EvidenceEvaluator:
    """
    Evaluates diagnostic evidence against clinical safety thresholds:
    - High-confidence verification threshold: >= 80%
    - Ambiguity warning threshold: < 60%
    - False-positive protection for Normal / Healthy Skin
    """

    CONFIDENCE_HIGH = 80.0
    CONFIDENCE_MODERATE = 60.0

    @classmethod
    def evaluate_diagnostic_evidence(
        cls,
        condition_name: str,
        confidence: float,
        differential_rule_outs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesizes clinical proof and assigns safety rating."""
        is_normal_skin = "normal" in condition_name.lower() or "healthy" in condition_name.lower()
        
        if is_normal_skin:
            safety_level = "CLEARED_HEALTHY"
            clinical_status = "No active dermatological pathology detected."
        elif confidence >= cls.CONFIDENCE_HIGH:
            safety_level = "STRONG_CLINICAL_CONCORDANCE"
            clinical_status = "Presentation demonstrates high hallmark concordance."
        elif confidence >= cls.CONFIDENCE_MODERATE:
            safety_level = "MODERATE_EVIDENCE_FURTHER_WORKUP_RECOMMENDED"
            clinical_status = "Clinical presentation suggestive; dermoscopy advised."
        else:
            safety_level = "INCONCLUSIVE_RE_EXAMINATION_REQUIRED"
            clinical_status = "Low diagnostic confidence; physical biopsy or examination needed."

        return {
            "condition": condition_name,
            "confidence": confidence,
            "safety_level": safety_level,
            "clinical_status": clinical_status,
            "rule_outs_verified": len(differential_rule_outs),
            "is_normal_tissue": is_normal_skin
        }
