# Using Your Own Model - Quick Guide

## Simple Steps

### 1. Place Your Model File

Copy your `.pt` model file to:
```
d:\Gui Weapon\models\weights\best.pt
```

**Important**: The file MUST be named `best.pt`

### 2. Run the Application

```bash
cd "d:\Gui Weapon"
run.bat
```

That's it! The system will automatically use your model.

---

## Model File Requirements

- **Format**: PyTorch model file (`.pt`)
- **Framework**: YOLOv8
- **Location**: `models/weights/best.pt`
- **Classes**: Should detect pistol and knife

---

## If You Don't Have a Model Yet

The system will automatically use a base YOLOv8 model for testing. You can:

1. Test the GUI and camera functionality
2. Later, when you have your model, just copy it to `models/weights/best.pt`
3. Restart the application

---

## Verification

After placing your model, run:
```bash
python test_system.py
```

It will show:
- ✓ Custom model found at models/weights/best.pt
- ✓ Model loaded successfully
- Model classes: [your classes]

---

## No Dataset or Training Needed

✓ No need to download any dataset
✓ No need to train any model
✓ Just place your `.pt` file and run
✓ System handles everything automatically

---

**Ready to use with your own model!**
