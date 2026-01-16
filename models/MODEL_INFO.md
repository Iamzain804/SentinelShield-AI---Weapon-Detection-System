# Model Configuration

## Current Model: best.pt

**Location:** `models/weights/best.pt`

**Classes:**
- Class 0: `pistol`
- Class 1: `knife`

**Total Classes:** 2

**Model Type:** YOLOv8n (lightweight, CPU-friendly)

**Parameters:** 3,011,238

---

## Important Notes:

1. ✅ System **ONLY** uses `best.pt` model
2. ❌ No fallback to other models
3. ⚠️ Model must exist at `models/weights/best.pt`
4. 🎯 Trained specifically for weapon detection

---

## Model Training Info:

This model is trained to detect:
- **Pistols** (handguns, revolvers)
- **Knives** (blades, cutting weapons)

The model is optimized for:
- ✅ Real-time detection
- ✅ CPU performance
- ✅ High accuracy on weapons
- ✅ Low false positives

---

## To Replace Model:

1. Train your own YOLOv8 model
2. Save it as `best.pt`
3. Copy to `models/weights/best.pt`
4. Restart the system

The system will automatically use your new model!

---

**Powered by SentinelShield AI**
