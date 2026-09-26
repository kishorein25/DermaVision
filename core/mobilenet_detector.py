import os
import logging
import torch
from PIL import Image
from torchvision import transforms

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "mobilenet_skin23.pt")
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])

DISPLAY = {
    "acne_and_rosacea": "Acne & Rosacea",
    "actinic_keratosis_basal_cell_carcinoma_and_other_malignant_lesions": "Actinic Keratosis / Skin Cancer",
    "atopic_dermatitis": "Atopic Dermatitis (Eczema)",
    "bullous_disease": "Bullous Disease (Blisters)",
    "cellulitis_impetigo_and_other_bacterial_infections": "Bacterial Skin Infection",
    "eczema": "Eczema",
    "exanthems_and_drug_eruptions": "Skin Rash / Drug Eruption",
    "hair_loss_photos_alopecia_and_other_hair_diseases": "Hair Loss / Alopecia",
    "herpes_hpv_and_other_stds": "Herpes / Viral Skin Infection",
    "light_diseases_and_disorders_of_pigmentation": "Hyperpigmentation (Dark Patches)",
    "lupus_and_other_connective_tissue_diseases": "Lupus / Connective Tissue Disease",
    "melanoma_skin_cancer_nevi_and_moles": "Melanoma / Moles",
    "nail_fungus_and_other_nail_disease": "Nail Fungus",
    "poison_ivy_photos_and_other_contact_dermatitis": "Contact Dermatitis",
    "psoriasis_pictures_lichen_planus_and_related_diseases": "Psoriasis / Lichen Planus",
    "scabies_lyme_disease_and_other_infestations_and_bites": "Scabies / Bites",
    "seborrheic_keratoses_and_other_benign_tumors": "Seborrheic Keratosis",
    "systemic_disease": "Systemic Disease",
    "tinea_ringworm_candidiasis_and_other_fungal_infections": "Ringworm / Fungal Infection",
    "urticaria_hives": "Urticaria (Hives)",
    "vascular_tumors": "Vascular Lesion",
    "vasculitis": "Vasculitis",
    "warts_molluscum_and_other_viral_infections": "Warts / Molluscum",
}

KB_MAP = {
    "acne_and_rosacea": "acne",
    "actinic_keratosis_basal_cell_carcinoma_and_other_malignant_lesions": "actinic_keratosis",
    "atopic_dermatitis": "eczema",
    "bullous_disease": "bullous_disease",
    "cellulitis_impetigo_and_other_bacterial_infections": "impetigo",
    "eczema": "eczema",
    "exanthems_and_drug_eruptions": "drug_eruption",
    "hair_loss_photos_alopecia_and_other_hair_diseases": "alopecia",
    "herpes_hpv_and_other_stds": "herpes_simplex",
    "light_diseases_and_disorders_of_pigmentation": "hyperpigmentation",
    "lupus_and_other_connective_tissue_diseases": "lupus",
    "melanoma_skin_cancer_nevi_and_moles": "melanoma",
    "nail_fungus_and_other_nail_disease": "nail_fungus",
    "poison_ivy_photos_and_other_contact_dermatitis": "contact_dermatitis",
    "psoriasis_pictures_lichen_planus_and_related_diseases": "psoriasis",
    "scabies_lyme_disease_and_other_infestations_and_bites": "scabies",
    "seborrheic_keratoses_and_other_benign_tumors": "seborrheic_keratosis",
    "systemic_disease": "systemic_disease",
    "tinea_ringworm_candidiasis_and_other_fungal_infections": "tinea_corporis",
    "urticaria_hives": "urticaria",
    "vascular_tumors": "vascular_lesion",
    "vasculitis": "vasculitis",
    "warts_molluscum_and_other_viral_infections": "molluscum_contagiosum",
}

_model = None
_classes = None


def is_available():
    return os.path.exists(MODEL_PATH)


def load_model():
    global _model, _classes
    if _model is None:
        if not is_available():
            logger.warning("MobileNet model not found: %s", MODEL_PATH)
            return None, None
        ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
        from torchvision import models
        net = models.mobilenet_v2(weights=None)
        net.classifier = torch.nn.Sequential(
            torch.nn.Dropout(0.3),
            torch.nn.Linear(net.last_channel, len(ckpt["classes"])),
        )
        net.load_state_dict(ckpt["state"])
        net.eval()
        _model, _classes = net, list(ckpt["classes"])
        logger.info("MobileNet loaded: %d classes", len(_classes))
    return _model, _classes


def predict(image, top_k=3):
    model, classes = load_model()
    if model is None:
        return None
    if isinstance(image, str):
        image = Image.open(image).convert("RGB")
    elif isinstance(image, Image.Image):
        image = image.convert("RGB")
    x = _transforms(image).unsqueeze(0)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=-1)[0]
    ordered = sorted(enumerate(probs.tolist()), key=lambda e: e[1], reverse=True)
    results = []
    for idx, conf in ordered[:top_k]:
        cls = classes[idx]
        results.append({
            "class": cls,
            "display": DISPLAY.get(cls, cls.replace("_", " ").title()),
            "std_key": KB_MAP.get(cls),
            "confidence": round(float(conf), 4),
        })
    return {"top": results, "label": results[0]["class"], "display": results[0]["display"],
            "std_key": results[0]["std_key"], "confidence": results[0]["confidence"]}