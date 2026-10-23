# ==============================================================================
# DermaVision: EfficientNetV2 Model Loader
# Singleton-safe, lazy-loading EfficientNetV2-S backbone for dermatological
# image classification. Mirrors the lazy-load pattern used in disease_engine.py.
#
# Supported freeze modes:
#   "classifier_only" — freezes all backbone layers, trains only head (Stage 1)
#   "partial"         — unfreezes last 2 feature blocks + head (Stage 2)
#   "none"            — all layers trainable (Stage 3 / full fine-tune)
# ==============================================================================

import os
import logging
from typing import Dict, List, Optional, Tuple, Any

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import EfficientNet_V2_S_Weights

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default constants
# ---------------------------------------------------------------------------
DEFAULT_VARIANT   = "efficientnet_v2_s"
DEFAULT_NUM_CLASSES = 23
DEFAULT_DEVICE    = "cpu"
DEFAULT_FREEZE    = "classifier_only"


class EfficientNetV2ModelLoader:
    """
    Singleton-safe loader for EfficientNetV2-S fine-tuned on skin disease data.

    Usage
    -----
    loader = EfficientNetV2ModelLoader(num_classes=23, weights_path="models/best.pth")
    model  = loader.get_model()   # loads on first call, cached thereafter
    """

    def __init__(
        self,
        model_variant: str = DEFAULT_VARIANT,
        num_classes: int = DEFAULT_NUM_CLASSES,
        weights_path: Optional[str] = None,
        device: str = DEFAULT_DEVICE,
        freeze_mode: str = DEFAULT_FREEZE,
    ) -> None:
        """
        Parameters
        ----------
        model_variant : str
            Currently only "efficientnet_v2_s" is supported.
        num_classes : int
            Number of output disease classes (23 per region, or 161 for all).
        weights_path : str, optional
            Path to a saved .pth checkpoint (state_dict).
            If None or file not found, falls back to ImageNet pretrained weights.
        device : str
            "cpu" or "cuda". Automatically falls back to CPU if CUDA unavailable.
        freeze_mode : str
            "classifier_only" | "partial" | "none"
        """
        self.model_variant  = model_variant
        self.num_classes    = num_classes
        self.weights_path   = weights_path
        self.freeze_mode    = freeze_mode
        self.device         = self._resolve_device(device)

        # Internal state
        self._model: Optional[nn.Module] = None
        self._is_loaded: bool = False
        self._loaded_from: str = ""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_model(self) -> nn.Module:
        """Returns the model, loading it on first call (lazy)."""
        if not self._is_loaded:
            self._load()
        return self._model  # type: ignore[return-value]

    def load(self) -> nn.Module:
        """Explicit load (same as get_model, provided for clarity)."""
        return self.get_model()

    def save_weights(self, path: str) -> None:
        """Saves model state_dict to disk."""
        if self._model is None:
            raise RuntimeError("[ModelLoader] Cannot save: model not loaded yet.")
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        torch.save(self._model.state_dict(), path)
        logger.info("[ModelLoader] Weights saved → %s", path)

    def load_weights(self, path: str) -> None:
        """
        Loads weights from a checkpoint into the current model.
        Triggers model build if not yet loaded.
        """
        if self._model is None:
            self._build_model(pretrained_imagenet=True)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"[ModelLoader] Checkpoint not found: {path}")
        state = torch.load(path, map_location=self.device)
        # Support both raw state_dict and {'model_state_dict': ...} wrapper
        if isinstance(state, dict) and "model_state_dict" in state:
            state = state["model_state_dict"]
        self._model.load_state_dict(state, strict=False)  # strict=False for head size mismatches
        self._loaded_from = path
        logger.info("[ModelLoader] Weights loaded from %s", path)

    def set_freeze_mode(self, freeze_mode: str) -> None:
        """
        Dynamically adjusts which layers are frozen/unfrozen.
        Useful for switching between training stages without re-instantiating.
        """
        self.freeze_mode = freeze_mode
        if self._model is not None:
            self._apply_freeze_mode(self._model)
            logger.info("[ModelLoader] Freeze mode set to: %s", freeze_mode)

    def get_model_info(self) -> Dict[str, Any]:
        """Returns a metadata dict describing the current loader state."""
        param_count = 0
        trainable_count = 0
        if self._model is not None:
            for p in self._model.parameters():
                param_count += p.numel()
                if p.requires_grad:
                    trainable_count += p.numel()
        return {
            "variant": self.model_variant,
            "num_classes": self.num_classes,
            "device": self.device,
            "freeze_mode": self.freeze_mode,
            "is_loaded": self._is_loaded,
            "loaded_from": self._loaded_from,
            "total_parameters": param_count,
            "trainable_parameters": trainable_count,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_device(self, requested: str) -> str:
        """Falls back to CPU if CUDA is requested but unavailable."""
        if requested == "cuda" and not torch.cuda.is_available():
            logger.warning("[ModelLoader] CUDA requested but not available. Falling back to CPU.")
            return "cpu"
        return requested

    def _load(self) -> None:
        """Full load sequence: build backbone → replace head → load weights → freeze."""
        try:
            # Step 1: Build EfficientNetV2-S with ImageNet pretrained weights
            model = self._build_model(pretrained_imagenet=True)

            # Step 2: Replace default 1000-class classifier with derma-specific head
            in_features = model.classifier[1].in_features
            model.classifier = nn.Sequential(
                nn.Dropout(p=0.3, inplace=True),
                nn.Linear(in_features, self.num_classes),
            )

            # Step 3: Apply layer freezing
            self._apply_freeze_mode(model)

            # Step 4: Move to device
            model = model.to(self.device)

            # Step 5: Load fine-tuned weights if a path was given
            if self.weights_path and os.path.isfile(self.weights_path):
                state = torch.load(self.weights_path, map_location=self.device)
                if isinstance(state, dict) and "model_state_dict" in state:
                    state = state["model_state_dict"]
                model.load_state_dict(state, strict=False)
                self._loaded_from = self.weights_path
                logger.info("[ModelLoader] Fine-tuned weights loaded from %s", self.weights_path)
            elif self.weights_path:
                logger.warning(
                    "[ModelLoader] Weights file not found at '%s'. "
                    "Using ImageNet pretrained backbone only.",
                    self.weights_path,
                )
                self._loaded_from = "imagenet_pretrained"
            else:
                self._loaded_from = "imagenet_pretrained"

            model.eval()
            self._model = model
            self._is_loaded = True
            logger.info(
                "[ModelLoader] EfficientNetV2-S ready | classes=%d | device=%s | freeze=%s",
                self.num_classes, self.device, self.freeze_mode,
            )

        except Exception as exc:
            self._is_loaded = False
            logger.error("[ModelLoader] Failed to load model: %s", exc)
            raise

    def _build_model(self, pretrained_imagenet: bool = True) -> nn.Module:
        """Constructs the EfficientNetV2-S backbone."""
        weights = EfficientNet_V2_S_Weights.IMAGENET1K_V1 if pretrained_imagenet else None
        return models.efficientnet_v2_s(weights=weights)

    def _apply_freeze_mode(self, model: nn.Module) -> None:
        """
        Freezes/unfreezes layers according to self.freeze_mode.

        EfficientNetV2-S feature blocks (model.features):
            [0]  Stem conv
            [1-6] MBConv blocks
            [7]  Last conv
        """
        if self.freeze_mode == "none":
            # All parameters trainable
            for param in model.parameters():
                param.requires_grad = True

        elif self.freeze_mode == "partial":
            # Freeze stem + first 5 blocks; unfreeze last 2 blocks + classifier
            for param in model.parameters():
                param.requires_grad = False
            # Unfreeze features[-2], features[-1] (blocks 6, 7), and classifier
            for param in model.features[-2].parameters():
                param.requires_grad = True
            for param in model.features[-1].parameters():
                param.requires_grad = True
            for param in model.classifier.parameters():
                param.requires_grad = True

        else:
            # Default: "classifier_only"
            # Freeze entire backbone, only train the new classification head
            for param in model.features.parameters():
                param.requires_grad = False
            for param in model.classifier.parameters():
                param.requires_grad = True

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        status = "loaded" if self._is_loaded else "not loaded"
        return (
            f"EfficientNetV2ModelLoader("
            f"variant={self.model_variant}, "
            f"num_classes={self.num_classes}, "
            f"device={self.device}, "
            f"freeze={self.freeze_mode}, "
            f"status={status})"
        )


# ---------------------------------------------------------------------------
# Convenience factory for most common use-case
# ---------------------------------------------------------------------------

def get_derma_model(
    num_classes: int = DEFAULT_NUM_CLASSES,
    weights_path: Optional[str] = None,
    device: str = DEFAULT_DEVICE,
) -> Tuple["EfficientNetV2ModelLoader", nn.Module]:
    """
    Factory shortcut: creates a loader and immediately returns the built model.

    Returns
    -------
    (loader, model) — loader is retained for weight-save / mode-switch ops.
    """
    loader = EfficientNetV2ModelLoader(
        num_classes=num_classes,
        weights_path=weights_path,
        device=device,
        freeze_mode="classifier_only",
    )
    model = loader.get_model()
    return loader, model


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json

    print("=" * 60)
    print("DermaVision EfficientNetV2ModelLoader — Smoke Test")
    print("=" * 60)

    loader = EfficientNetV2ModelLoader(
        num_classes=23,
        weights_path=None,
        device="cpu",
        freeze_mode="classifier_only",
    )
    model = loader.get_model()
    info = loader.get_model_info()
    print(json.dumps(info, indent=2))

    # Verify output shape
    dummy = torch.zeros(1, 3, 224, 224)
    with torch.no_grad():
        out = model(dummy)
    print(f"\nOutput tensor shape: {out.shape}  ← expected [1, 23]")
    assert out.shape == (1, 23), "Shape mismatch!"
    print("\n✅ EfficientNetV2ModelLoader: PASS")
