import os
import json
import logging
from PIL import Image
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PRIMARY_MODEL = "Jayanth2002/dinov2-base-finetuned-SkinDisease"
SECONDARY_MODEL = "Jayanth2002/vit_base_patch16_224-finetuned-SkinDisease"

CONFIDENCE_THRESHOLD = 0.35

_primary = None
_primary_proc = None
_secondary = None
_secondary_proc = None

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def _load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_primary():
    global _primary, _primary_proc
    if _primary is None:
        from transformers import AutoImageProcessor, AutoModelForImageClassification
        logger.info("Loading PRIMARY model: %s", PRIMARY_MODEL)
        _primary_proc = AutoImageProcessor.from_pretrained(PRIMARY_MODEL)
        _primary = AutoModelForImageClassification.from_pretrained(PRIMARY_MODEL)
        _primary.eval()
        if torch.cuda.is_available():
            _primary = _primary.cuda()
    return _primary, _primary_proc


def load_secondary():
    global _secondary, _secondary_proc
    if _secondary is None:
        from transformers import AutoImageProcessor, AutoModelForImageClassification
        logger.info("Loading SECONDARY model: %s", SECONDARY_MODEL)
        _secondary_proc = AutoImageProcessor.from_pretrained(SECONDARY_MODEL)
        _secondary = AutoModelForImageClassification.from_pretrained(SECONDARY_MODEL)
        _secondary.eval()
        if torch.cuda.is_available():
            _secondary = _secondary.cuda()
    return _secondary, _secondary_proc


def load_models():
    load_primary()
    load_secondary()
    logger.info("Both models loaded successfully")


def preprocess_image(image):
    if isinstance(image, str):
        return Image.open(image).convert("RGB")
    if isinstance(image, Image.Image):
        return image.convert("RGB")
    raise ValueError("Unsupported image type")


def _predict(model, processor, image):
    device = next(model.parameters()).device
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[0]
    return probs.cpu().numpy()


def get_top_predictions(model, processor, image, top_k=3):
    probs = _predict(model, processor, image)
    model_id2label = model.config.id2label
    ordered = sorted(enumerate(probs.tolist()), key=lambda x: x[1], reverse=True)
    results = []
    for idx, conf in ordered[:top_k]:
        label = model_id2label.get(str(idx), model_id2label.get(idx, f"class_{idx}"))
        results.append({"label": label, "confidence": float(conf)})
    return results, probs


def detect_with_both(image, top_k=3):
    """Runs both PRIMARY and SECONDARY models and combines their results."""
    primary_model, primary_proc = load_primary()
    secondary_model, secondary_proc = load_secondary()

    img = preprocess_image(image)

    primary_results, primary_probs = get_top_predictions(primary_model, primary_proc, img, top_k)
    secondary_results, secondary_probs = get_top_predictions(secondary_model, secondary_proc, img, top_k)

    primary_label = primary_results[0]["label"]
    primary_conf = primary_results[0]["confidence"]

    # Find matching secondary result (same or similar label)
    secondary_label = secondary_results[0]["label"]
    secondary_conf = secondary_results[0]["confidence"]

    # Determine if models agree (same label or label in each other's top-3)
    agreed = False
    matched_conf_2 = None
    for r in secondary_results:
        if _normalize_label(r["label"]) == _normalize_label(primary_label):
            agreed = True
            matched_conf_2 = r["confidence"]
            secondary_label = r["label"]
            secondary_conf = r["confidence"]
            break

    # Combined confidence: average if agree, lower if disagree
    if agreed:
        combined_conf = (primary_conf + secondary_conf) / 2
    else:
        combined_conf = primary_conf * 0.6

    result = {
        "primary_label": primary_label,
        "primary_confidence": round(primary_conf, 4),
        "secondary_label": secondary_label,
        "secondary_confidence": round(secondary_conf, 4),
        "agreed": agreed,
        "combined_confidence": round(combined_conf, 4),
        "primary_top3": primary_results,
        "secondary_top3": secondary_results,
        "is_normal": combined_conf < CONFIDENCE_THRESHOLD,
    }

    result["final_label"] = primary_label if agreed or not secondary_label else (
        primary_label if primary_conf >= secondary_conf else secondary_label
    )

    return result


def _normalize_label(label):
    s = str(label).strip().lower()
    s = s.replace("_", " ").replace("-", " ").replace(".", "")
    return " ".join(s.split())


def map_hf_to_standard(label):
    """Maps HuggingFace 31-class labels to our standard disease keys."""
    mapping = {
        "actinic keratosis": "actinic_keratosis",
        "basal cell carcinoma": "basal_cell_carcinoma",
        "darier_s disease": "darier_disease",
        "dermatofibroma": "dermatofibroma",
        "epidermolysis bullosa pruriginosa": "epidermolysis_bullosa",
        "hailey-hailey disease": "hailey_hailey",
        "herpes simplex": "herpes_simplex",
        "impetigo": "impetigo",
        "larva migrans": "larva_migrans",
        "leprosy borderline": "leprosy",
        "leprosy lepromatous": "leprosy",
        "leprosy tuberculoid": "leprosy",
        "lichen planus": "lichen_planus",
        "lupus erythematosus chronicus discoides": "lupus",
        "melanoma": "melanoma",
        "molluscum contagiosum": "molluscum_contagiosum",
        "mycosis fungoides": "mycosis_fungoides",
        "neurofibromatosis": "neurofibromatosis",
        "papilomatosis confluentes and reticulate": "papilomatosis",
        "pediculosis capitis": "pediculosis_capitis",
        "pityriasis rosea": "pityriasis_rosea",
        "porokeratosis actinic": "porokeratosis",
        "psoriasis": "psoriasis",
        "seborrheic keratosis": "seborrheic_keratosis",
        "squamous cell carcinoma": "squamous_cell_carcinoma",
        "tinea corporis": "tinea_corporis",
        "tinea nigra": "tinea_nigra",
        "tungiasis": "tungiasis",
        "vascular lesion": "vascular_lesion",
        "nevus": "nevus",
        "pigmented benign keratosis": "pigmented_benign_keratosis",
    }
    return mapping.get(_normalize_label(label), None)