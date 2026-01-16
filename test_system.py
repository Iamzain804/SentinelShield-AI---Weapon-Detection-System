"""
Quick Test Script for Weapon Detection System
Tests GPU, camera, and basic detection functionality
"""

import sys
import torch
import cv2
from pathlib import Path

def test_gpu():
    """Test GPU availability"""
    print("\n" + "="*60)
    print("GPU Test")
    print("="*60)
    
    if torch.cuda.is_available():
        print(f"✓ GPU Available: {torch.cuda.get_device_name(0)}")
        print(f"✓ CUDA Version: {torch.version.cuda}")
        print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        return True
    else:
        print("✗ No GPU detected")
        print("  The system will work but will be slower on CPU")
        return False

def test_camera():
    """Test camera availability"""
    print("\n" + "="*60)
    print("Camera Test")
    print("="*60)
    
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✓ Camera {i} working - Resolution: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
            else:
                print(f"✗ Camera {i} found but cannot read frames")
                cap.release()
        else:
            if i == 0:
                print(f"✗ No camera found at index {i}")

def test_dependencies():
    """Test required dependencies"""
    print("\n" + "="*60)
    print("Dependencies Test")
    print("="*60)
    
    dependencies = {
        'torch': 'PyTorch',
        'cv2': 'OpenCV',
        'ultralytics': 'YOLOv8',
        'PyQt5': 'PyQt5',
        'PIL': 'Pillow',
        'numpy': 'NumPy'
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} NOT installed")
            all_ok = False
    
    return all_ok

def test_model():
    """Test model loading"""
    print("\n" + "="*60)
    print("Model Test")
    print("="*60)
    
    model_path = Path("models/weights/best.pt")
    
    if model_path.exists():
        print(f"✓ Trained model found at {model_path}")
        try:
            from ultralytics import YOLO
            model = YOLO(str(model_path))
            print("✓ Model loaded successfully")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            return False
    else:
        print(f"✗ Trained model not found at {model_path}")
        print("  Will use pretrained YOLOv8n for testing")
        return False

def test_alert_system():
    """Test alert system"""
    print("\n" + "="*60)
    print("Alert System Test")
    print("="*60)
    
    alerts_folder = Path("alerts")
    if alerts_folder.exists():
        print(f"✓ Alerts folder exists")
    else:
        print(f"✗ Alerts folder not found (will be created automatically)")
    
    sound_file = Path("assets/alert.wav")
    if sound_file.exists():
        print(f"✓ Alert sound file exists")
        try:
            import pygame
            pygame.mixer.init()
            sound = pygame.mixer.Sound(str(sound_file))
            print("✓ Sound system working")
        except Exception as e:
            print(f"✗ Sound system error: {e}")
    else:
        print(f"✗ Alert sound not found at {sound_file}")

def main():
    print("\n" + "="*60)
    print("Hanif Jewellery - Weapon Detection System Test")
    print("="*60)
    
    # Run tests
    gpu_ok = test_gpu()
    deps_ok = test_dependencies()
    test_camera()
    test_model()
    test_alert_system()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    if deps_ok:
        print("✓ All dependencies installed")
    else:
        print("✗ Some dependencies missing - run setup.bat")
    
    if gpu_ok:
        print("✓ GPU acceleration available")
    else:
        print("⚠ GPU not available - system will be slower")
    
    print("\n" + "="*60)
    print("Ready to run: python src\\gui_main.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
