"""
TreatmentProtocols: Pharmacological & Clinical Reference Library
Categorizes first-line topical therapies, oral regimens, and non-pharmacological care.
"""

from typing import Dict, Any

class TreatmentProtocols:
    """
    Standardized dermatological management guidelines derived from AAD/BAD protocols.
    Includes mandatory medical alerts against self-prescribing potent steroids or retinoids.
    """

    @classmethod
    def get_clinical_alert_badge(cls) -> str:
        """Returns standard physician alert warning text."""
        return (
            "⚠️ CLINICAL ADVISORY: Do not initiate potent prescription corticosteroids or systemic retinoids "
            "without direct dermatological supervision. Inappropriate topical application can induce skin atrophy, "
            "telangiectasia, or steroid rosacea."
        )

    @classmethod
    def format_treatment_summary(cls, condition_name: str, region: str) -> Dict[str, str]:
        """Provides structured therapeutic category outlines."""
        return {
            "first_line_topical": f"Targeted topical agents calibrated for {region} epidermal thickness.",
            "lifestyle_barrier": "Gentle non-soap syndet cleanser, barrier repair ceramide moisturizers, broad-spectrum SPF 50+.",
            "physician_warning": cls.get_clinical_alert_badge()
        }
