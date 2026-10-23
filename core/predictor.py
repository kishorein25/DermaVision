# ==============================================================================
# DermaVision: EfficientNetV2 Predictor — Inference & Grad-CAM Heatmap Engine
#
# Provides:
#   1. Standardized preprocessing pipeline (CLAHE → bilateral → tensor)
#   2. EfficientNetV2 inference with softmax confidence ranking
#   3. Grad-CAM Class Activation Map overlay generation
#
# Designed as a standalone module — does NOT modify disease_engine.py or any
# existing module. Can be optionally integrated as a 3rd signal in the engine.
# ==============================================================================

import io
import logging
from typing import Dict, List, Optional, Any, Tuple

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from .model_loader import EfficientNetV2ModelLoader
from .vision_processor import VisionProcessor

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ImageNet normalization constants (EfficientNetV2-S standard)
# ---------------------------------------------------------------------------
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]
INPUT_SIZE    = 224


class DermaPredictor:
    """
    Inference engine for the EfficientNetV2-S dermatological classifier.

    Parameters
    ----------
    model_loader : EfficientNetV2ModelLoader
        Pre-configured loader — the model is pulled via loader.get_model().
    class_names : list[str]
        Ordered list of disease class names matching the model's output neurons.
        Index 0 → output neuron 0.
    device : str
        "cpu" or "cuda".

    Example
    -------
    >>> from core.model_loader import EfficientNetV2ModelLoader
    >>> from config import CONDITIONS_DB
    >>> class_names = [c["name"] for c in CONDITIONS_DB["Face"]]
    >>> loader = EfficientNetV2ModelLoader(num_classes=23)
    >>> predictor = DermaPredictor(loader, class_names)
    >>> result = predictor.predict(pil_image)
    >>> result_with_cam = predictor.predict_with_gradcam(pil_image)
    """

    def __init__(
        self,
        model_loader: EfficientNetV2ModelLoader,
        class_names: List[str],
        device: str = "cpu",
    ) -> None:
        self.loader      = model_loader
        self.class_names = class_names
        self.device      = device
        self._model: Optional[nn.Module] = None

        # Grad-CAM state — populated during forward/backward hooks
        self._gradcam_gradients: Optional[torch.Tensor] = None
        self._gradcam_activations: Optional[torch.Tensor] = None
        self._hook_handles: List[Any] = []

        # Preprocessing transform (applied after CLAHE + bilateral)
        self._transform = transforms.Compose([
            transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def preprocess(self, pil_image: Image.Image) -> torch.Tensor:
        """
        Full clinical preprocessing pipeline:
          1. PIL → OpenCV BGR
          2. CLAHE illumination normalization (from VisionProcessor)
          3. Bilateral edge-preserving denoising
          4. Resize to 224×224
          5. ToTensor + ImageNet normalization

        Returns
        -------
        torch.Tensor of shape [1, 3, 224, 224]
        """
        # Step 1-3: Clinical OpenCV preprocessing
        bgr = VisionProcessor.pil_to_cv2(pil_image)
        bgr_preprocessed, _ = VisionProcessor.preprocess_clinical_image(bgr, target_max_dim=512)
        pil_clean = VisionProcessor.cv2_to_pil(bgr_preprocessed)

        # Step 4-5: Resize, normalize, add batch dim
        tensor = self._transform(pil_clean).unsqueeze(0).to(self.device)
        return tensor

    def predict(
        self,
        pil_image: Image.Image,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Runs EfficientNetV2 inference on the input image.

        Returns
        -------
        dict with keys:
            "class_name"   : str  — predicted class label
            "class_idx"    : int  — output neuron index
            "confidence"   : float — softmax probability (0–100)
            "top_k"        : list[dict] — top-k {class_name, confidence} entries
            "all_probs"    : dict[str, float] — full softmax distribution
        """
        model = self._get_model()
        model.eval()

        tensor = self.preprocess(pil_image)

        with torch.no_grad():
            logits = model(tensor)                    # [1, num_classes]
            probs  = F.softmax(logits, dim=1)[0]      # [num_classes]

        probs_np = probs.cpu().numpy()
        top_idx  = int(np.argmax(probs_np))
        top_conf = float(probs_np[top_idx]) * 100.0

        # Build top-k list
        sorted_indices = np.argsort(probs_np)[::-1]
        top_k_list = []
        for i in range(min(top_k, len(self.class_names))):
            idx = sorted_indices[i]
            top_k_list.append({
                "rank":        i + 1,
                "class_name":  self.class_names[idx],
                "class_idx":   int(idx),
                "confidence":  round(float(probs_np[idx]) * 100.0, 2),
            })

        # Full distribution
        all_probs = {
            self.class_names[i]: round(float(probs_np[i]) * 100.0, 2)
            for i in range(len(self.class_names))
        }

        return {
            "class_name":  self.class_names[top_idx],
            "class_idx":   top_idx,
            "confidence":  round(top_conf, 2),
            "top_k":       top_k_list,
            "all_probs":   all_probs,
        }

    def generate_gradcam(
        self,
        pil_image: Image.Image,
        target_class_idx: Optional[int] = None,
        alpha: float = 0.45,
    ) -> Optional[Image.Image]:
        """
        Generates a Grad-CAM Class Activation Map and overlays it on the image.

        The target convolutional layer is the last feature block of EfficientNetV2-S
        (model.features[-1]), which contains rich high-level semantic activations.

        Parameters
        ----------
        pil_image : PIL.Image
            Original input clinical image.
        target_class_idx : int, optional
            Class index to compute gradients for.
            If None, uses the argmax predicted class.
        alpha : float
            Blending weight for heatmap overlay (0.0 = image only, 1.0 = heatmap only).

        Returns
        -------
        PIL.Image with jet colormap heatmap blended over the original,
        or None if CAM generation fails (graceful degradation).
        """
        try:
            model = self._get_model()
            model.eval()

            # Register hooks on the last feature block
            self._register_gradcam_hooks(model)

            tensor = self.preprocess(pil_image)
            tensor.requires_grad_(True)

            # Forward pass
            logits = model(tensor)
            probs  = F.softmax(logits, dim=1)[0]

            if target_class_idx is None:
                target_class_idx = int(probs.argmax().item())

            # Backward pass for the target class
            model.zero_grad()
            score = logits[0, target_class_idx]
            score.backward()

            # Retrieve stored gradients and activations
            gradients  = self._gradcam_gradients    # [1, C, H, W]
            activations = self._gradcam_activations  # [1, C, H, W]

            if gradients is None or activations is None:
                self._remove_hooks()
                return None

            # Global average pool the gradients → channel weights [C]
            weights = gradients.mean(dim=(2, 3), keepdim=True)  # [1, C, 1, 1]

            # Weighted sum of activation maps
            cam = (weights * activations).sum(dim=1, keepdim=True)  # [1, 1, H, W]
            cam = F.relu(cam)

            # Normalize to [0, 1]
            cam_np = cam.squeeze().detach().cpu().numpy()
            cam_np -= cam_np.min()
            if cam_np.max() > 0:
                cam_np /= cam_np.max()

            # Resize CAM to original image size
            orig_w, orig_h = pil_image.size
            cam_resized = cv2.resize(cam_np, (orig_w, orig_h), interpolation=cv2.INTER_CUBIC)

            # Apply jet colormap
            heatmap_uint8  = np.uint8(255 * cam_resized)
            heatmap_color  = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
            heatmap_rgb    = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

            # Blend with original image
            original_np = np.array(pil_image.convert("RGB"))
            overlay     = cv2.addWeighted(original_np, 1.0 - alpha, heatmap_rgb, alpha, 0)

            self._remove_hooks()
            return Image.fromarray(overlay)

        except Exception as exc:
            logger.warning("[DermaPredictor] Grad-CAM generation failed: %s", exc)
            self._remove_hooks()
            return None

    def predict_with_gradcam(
        self,
        pil_image: Image.Image,
        top_k: int = 5,
        cam_alpha: float = 0.45,
    ) -> Dict[str, Any]:
        """
        Convenience method: runs prediction then generates Grad-CAM for the top class.

        Returns
        -------
        dict with keys:
            "prediction"  : dict — same as predict() output
            "heatmap"     : PIL.Image or None — Grad-CAM overlay image
            "target_class": str — class used for CAM generation
        """
        prediction = self.predict(pil_image, top_k=top_k)
        target_idx = prediction["class_idx"]

        heatmap = self.generate_gradcam(
            pil_image,
            target_class_idx=target_idx,
            alpha=cam_alpha,
        )

        return {
            "prediction":   prediction,
            "heatmap":      heatmap,
            "target_class": prediction["class_name"],
        }

    # ------------------------------------------------------------------
    # Grad-CAM hook management (private)
    # ------------------------------------------------------------------

    def _register_gradcam_hooks(self, model: nn.Module) -> None:
        """Attaches forward + backward hooks on the last EfficientNet feature block."""
        self._gradcam_gradients  = None
        self._gradcam_activations = None
        self._remove_hooks()

        target_layer = model.features[-1]

        def forward_hook(module, input, output):
            self._gradcam_activations = output

        def backward_hook(module, grad_input, grad_output):
            self._gradcam_gradients = grad_output[0]

        self._hook_handles.append(
            target_layer.register_forward_hook(forward_hook)
        )
        self._hook_handles.append(
            target_layer.register_full_backward_hook(backward_hook)
        )

    def _remove_hooks(self) -> None:
        """Removes all registered hooks to avoid memory leaks."""
        for handle in self._hook_handles:
            handle.remove()
        self._hook_handles.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_model(self) -> nn.Module:
        """Returns the model from loader, caching it locally."""
        if self._model is None:
            self._model = self.loader.get_model()
        return self._model

    def __repr__(self) -> str:
        return (
            f"DermaPredictor("
            f"classes={len(self.class_names)}, "
            f"device={self.device}, "
            f"model={self.loader.model_variant})"
        )


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from core.model_loader import EfficientNetV2ModelLoader

    print("=" * 60)
    print("DermaPredictor — Smoke Test")
    print("=" * 60)

    # Dummy 23-class names
    class_names = [f"Disease_{i+1}" for i in range(23)]

    loader    = EfficientNetV2ModelLoader(num_classes=23, device="cpu")
    predictor = DermaPredictor(loader, class_names, device="cpu")

    # Synthetic 224x224 test image
    dummy_img = Image.fromarray(np.random.randint(100, 200, (224, 224, 3), dtype=np.uint8))

    # Test predict
    result = predictor.predict(dummy_img, top_k=3)
    print(f"\nPrediction: {result['class_name']}  ({result['confidence']:.1f}%)")
    print(f"Top-3: {[(r['class_name'], r['confidence']) for r in result['top_k']]}")

    # Test Grad-CAM
    cam_result = predictor.predict_with_gradcam(dummy_img)
    cam_img    = cam_result["heatmap"]
    print(f"\nGrad-CAM: {'Generated OK' if cam_img is not None else 'None (graceful fallback)'}")
    if cam_img:
        print(f"CAM image size: {cam_img.size}")

    print("\n✅ DermaPredictor: PASS")
