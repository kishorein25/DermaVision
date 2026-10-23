# 🔬 DermaVision `core/` Vision Engine

This package encapsulates low-level computer vision, image processing, landmark geometry, and optical dermatological feature extraction algorithms.

---

## 📂 Modules & Architecture

```
core/
├── __init__.py               # Package exposure for core pipeline
├── vision_processor.py       # CLAHE, bilateral edge-preserving smoothing, and color space transforms
├── landmark_geometry.py      # 468-point 3D landmark geometric vector calculations, face bounds & pose
├── texture_analyzer.py       # Local variance, sharpness, and micro-relief surface roughness profiling
├── color_segmentation.py     # Fitzpatrick-invariant skin masking, Erythema Index (EI) & Melanin Index (MI)
└── README.md                 # This technical documentation
```

---

## ⚡ Key Mathematical & Algorithmic Foundations

1. **CLAHE Illumination Equalization (`vision_processor.py`)**:
   Standardizes varying ambient lighting in clinic photographs across L* channel in CIELAB space without degrading Fitzpatrick skin tone fidelity.

2. **3D Pose & Facial Bounds (`landmark_geometry.py`)**:
   Computes vector roll, pitch, and yaw from MediaPipe 468 3D points. Guarantees the target anatomical area is oriented within diagnostic limits.

3. **Lesion Texture & Micro-Relief (`texture_analyzer.py`)**:
   Applies high-frequency Laplacian variance and local variance kernels to differentiate smooth epidermis from hyperkeratotic plaque and papular lesions.

4. **Erythema & Melanin Indices (`color_segmentation.py`)**:
   Implements optical absorption equations:
   $$\text{Erythema Index (EI)} = 100 \times [\log_{10}(1/G) - \log_{10}(1/R)]$$
   $$\text{Melanin Index (MI)} = 100 \times \log_{10}(1/R)$$
