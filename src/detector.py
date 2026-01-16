"""
Weapon Detection Engine - CPU Only Version
Real-time detection using YOLOv8 on CPU
Detects: Pistol, Knife
"""

import cv2
from ultralytics import YOLO
import numpy as np
from pathlib import Path
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeaponDetector:
    def __init__(self, model_path="../models/weights/best.pt", confidence_threshold=0.5):
        """
        Initialize Weapon Detector - CPU Only Version
        
        Args:
            model_path: Path to trained YOLOv8 model (relative to src/ directory)
            confidence_threshold: Minimum confidence for detection (0.0 to 1.0)
        """
        # Validate confidence threshold
        if not 0.0 <= confidence_threshold <= 1.0:
            logger.warning(f"Invalid confidence threshold {confidence_threshold}, using 0.5")
            confidence_threshold = 0.5
        
        self.model_path = Path(model_path)
        self.confidence_threshold = confidence_threshold
        
        # CPU only mode
        self.device = 'cpu'
        logger.info("Running in CPU-only mode")
        
        # Load model with error handling
        self.model = None
        self.model_loaded = False
        self.load_model()
        
        # Class names - can be customized based on model
        self.class_names = ['pistol', 'knife']
        
        # Colors for bounding boxes (BGR format)
        self.colors = {
            'pistol': (0, 0, 255),      # Red
            'knife': (0, 165, 255),     # Orange
            'default': (0, 255, 255)    # Yellow for unknown classes
        }
        
        # Detection statistics
        self.total_detections = 0
        self.frame_count = 0
        self.error_count = 0
    
    def load_model(self):
        """Load YOLOv8 model - Only uses best.pt (No Fallback)"""
        try:
            # Only use the trained weapon detection model
            if self.model_path.exists():
                logger.info(f"Loading weapon detection model from {self.model_path}")
                try:
                    self.model = YOLO(str(self.model_path))
                    self.model.to(self.device)
                    logger.info("✓ Weapon detection model loaded successfully!")
                    self.model_loaded = True
                    
                    # Get class names from model
                    if hasattr(self.model, 'names'):
                        self.class_names = list(self.model.names.values())
                        logger.info(f"✓ Model classes: {self.class_names}")
                    
                    return
                except Exception as e:
                    logger.error(f"Failed to load model: {e}")
                    self.model = None
                    self.model_loaded = False
                    logger.error("Cannot proceed without the model!")
                    return
            else:
                # Model not found - CRITICAL ERROR
                logger.error(f"CRITICAL: Model not found at {self.model_path}")
                logger.error("Please place your trained model at: models/weights/best.pt")
                self.model = None
                self.model_loaded = False
            
        except Exception as e:
            logger.error(f"CRITICAL: Failed to load model: {e}")
            self.model = None
            self.model_loaded = False
            logger.error("Detection will not work without a model!")
    
    def detect(self, frame):
        """
        Perform weapon detection on frame with comprehensive error handling
        
        Args:
            frame: Input video frame (BGR format, numpy array)
        
        Returns:
            annotated_frame: Frame with bounding boxes and labels
            detections: List of detected class names
            confidence_scores: List of confidence scores
            has_detection: Boolean indicating if any weapon was detected
        """
        # Validate input frame
        if frame is None:
            logger.error("Received None frame")
            return np.zeros((480, 640, 3), dtype=np.uint8), [], [], False
        
        if not isinstance(frame, np.ndarray):
            logger.error(f"Invalid frame type: {type(frame)}")
            return frame if isinstance(frame, np.ndarray) else np.zeros((480, 640, 3), dtype=np.uint8), [], [], False
        
        if frame.size == 0:
            logger.error("Received empty frame")
            return np.zeros((480, 640, 3), dtype=np.uint8), [], [], False
        
        # Check if model is loaded
        if not self.model_loaded or self.model is None:
            logger.warning("Model not loaded, returning original frame")
            return frame.copy(), [], [], False
        
        self.frame_count += 1
        
        detections = []
        confidence_scores = []
        has_detection = False
        annotated_frame = frame.copy()
        
        try:
            # Run inference with error handling
            results = self.model(
                frame, 
                conf=self.confidence_threshold, 
                device=self.device, 
                verbose=False
            )
            
            # Process results safely
            for result in results:
                try:
                    boxes = result.boxes
                    
                    if boxes is None or len(boxes) == 0:
                        continue
                    
                    has_detection = True
                    
                    for box in boxes:
                        try:
                            # Get box coordinates
                            xyxy = box.xyxy[0].numpy() if hasattr(box.xyxy[0], 'numpy') else box.xyxy[0]
                            x1, y1, x2, y2 = map(int, xyxy)
                            
                            # Validate coordinates
                            h, w = frame.shape[:2]
                            x1, y1 = max(0, x1), max(0, y1)
                            x2, y2 = min(w, x2), min(h, y2)
                            
                            # Get confidence and class
                            conf_tensor = box.conf[0]
                            confidence = float(conf_tensor.numpy() if hasattr(conf_tensor, 'numpy') else conf_tensor)
                            
                            cls_tensor = box.cls[0]
                            class_id = int(cls_tensor.numpy() if hasattr(cls_tensor, 'numpy') else cls_tensor)
                            
                            # Get class name safely
                            if hasattr(self.model, 'names') and class_id in self.model.names:
                                class_name = self.model.names[class_id]
                            elif class_id < len(self.class_names):
                                class_name = self.class_names[class_id]
                            else:
                                class_name = f"Object_{class_id}"
                            
                            # Add to detections
                            detections.append(class_name)
                            confidence_scores.append(confidence)
                            self.total_detections += 1
                            
                            # Get color
                            color = self.colors.get(class_name.lower(), self.colors.get('default', (0, 255, 255)))
                            
                            # Draw bounding box
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 3)
                            
                            # Draw label background
                            label = f"{class_name.upper()}: {confidence:.2%}"
                            (label_w, label_h), _ = cv2.getTextSize(
                                label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2
                            )
                            
                            # Ensure label fits in frame
                            label_y = max(label_h + 10, y1)
                            cv2.rectangle(
                                annotated_frame, 
                                (x1, label_y - label_h - 10), 
                                (min(x1 + label_w, w), label_y), 
                                color, 
                                -1
                            )
                            
                            # Draw label text
                            cv2.putText(
                                annotated_frame, 
                                label, 
                                (x1, label_y - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.8, 
                                (255, 255, 255), 
                                2
                            )
                            
                        except Exception as box_error:
                            logger.error(f"Error processing box: {box_error}")
                            continue
                    
                except Exception as result_error:
                    logger.error(f"Error processing result: {result_error}")
                    continue
            
            # Add red border if detection
            if has_detection:
                h, w = annotated_frame.shape[:2]
                cv2.rectangle(annotated_frame, (0, 0), (w-1, h-1), (0, 0, 255), 10)
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            self.error_count += 1
            # Return original frame on error
            return frame.copy(), [], [], False
        
        return annotated_frame, detections, confidence_scores, has_detection
    
    def get_stats(self):
        """Get detection statistics"""
        return {
            'total_detections': self.total_detections,
            'frames_processed': self.frame_count,
            'device': self.device
        }
    
    def reset_stats(self):
        """Reset detection statistics"""
        self.total_detections = 0
        self.frame_count = 0
