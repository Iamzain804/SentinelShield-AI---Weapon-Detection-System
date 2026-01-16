"""
Check Model Information
Shows what classes are in the trained model
"""

from ultralytics import YOLO
from pathlib import Path

def check_model(model_path="models/weights/best.pt"):
    """Check model details"""
    
    model_file = Path(model_path)
    
    print("\n" + "="*60)
    print("Model Information Checker")
    print("="*60)
    
    if not model_file.exists():
        print(f"❌ Model not found at: {model_path}")
        print("\nUsing default YOLOv8n instead...")
        model_path = "yolov8n.pt"
    else:
        print(f"✓ Model found: {model_path}")
    
    print("\nLoading model...")
    try:
        model = YOLO(model_path)
        
        print("\n" + "="*60)
        print("Model Details")
        print("="*60)
        
        # Get class names
        if hasattr(model, 'names'):
            class_names = model.names
            print(f"\nTotal Classes: {len(class_names)}")
            print("\nClass List:")
            print("-" * 40)
            for idx, name in class_names.items():
                print(f"  {idx}: {name}")
            print("-" * 40)
        else:
            print("❌ Cannot retrieve class names")
        
        # Model info
        print(f"\nModel Type: {model.task}")
        print(f"Model File: {model_path}")
        
        # Try to get more info
        if hasattr(model, 'model'):
            try:
                total_params = sum(p.numel() for p in model.model.parameters())
                print(f"Total Parameters: {total_params:,}")
            except:
                pass
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Error loading model: {e}")
    
    print()

if __name__ == "__main__":
    import sys
    
    # Check if custom path provided
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    else:
        model_path = "../models/weights/best.pt"
    
    check_model(model_path)
