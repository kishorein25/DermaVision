"""
DietaryGuidelines: Evidence-Based Dermatological Nutritional Guidance
Maps common dermatological conditions to anti-inflammatory foods and known inflammatory triggers.
"""

from typing import Dict, Tuple

class DietaryGuidelines:
    """
    Evidence-based dietary protocols for dermatological health:
    - Acne: low-glycemic, reduced dairy, omega-3 fatty acids
    - Eczema/Atopic: anti-histaminic, omega-3, quercetin-rich foods
    - Psoriasis: anti-inflammatory Mediterranean diet, reduced alcohol
    - General: hydration, zinc, vitamins A, C, E
    """

    PROTOCOLS: Dict[str, Tuple[str, str]] = {
        "acne": (
            "Omega-3 fatty acids (flaxseeds, walnuts, wild salmon), green tea, probiotic yogurt, zinc-rich pumpkin seeds, leafy greens.",
            "High-glycemic sugars, processed snacks, skim milk, whey protein supplements, excessive fried or oily foods."
        ),
        "eczema": (
            "Quercetin-rich blueberries, spinach, chamomile infusion, fatty fish, vitamin D fortified foods.",
            "High-histamine aged cheeses, artificial preservatives, gluten (if sensitive), extreme spicy condiments."
        ),
        "psoriasis": (
            "Mediterranean diet, extra virgin olive oil, turmeric (curcumin), leafy cruciferous vegetables, berries.",
            "Alcohol, processed red meats, refined white flours, nightshades (if patient exhibits personal sensitivity)."
        ),
        "fungal": (
            "Garlic (allicin), coconut oil (caprylic acid), unsweetened kefir, fibrous prebiotic vegetables.",
            "Refined sucrose, yeast-dense pastries, sugary carbonated beverages, excessive beer."
        )
    }

    @classmethod
    def get_guidelines_for_condition(cls, condition_name: str) -> Tuple[str, str]:
        """Returns (recommended_foods, foods_to_avoid) based on condition classification."""
        c_lower = condition_name.lower()
        if "acne" in c_lower or "folliculitis" in c_lower:
            return cls.PROTOCOLS["acne"]
        elif "eczema" in c_lower or "dermatitis" in c_lower:
            return cls.PROTOCOLS["eczema"]
        elif "psoriasis" in c_lower:
            return cls.PROTOCOLS["psoriasis"]
        elif "tinea" in c_lower or "ringworm" in c_lower or "candidiasis" in c_lower:
            return cls.PROTOCOLS["fungal"]

        return (
            "Antioxidant-rich colorful berries, zinc-rich seeds, dark leafy greens, plenty of pure water (2-3 L/day).",
            "Ultra-processed convenience foods, high-sugar confectioneries, excess sodium, artificial flavor enhancers."
        )
