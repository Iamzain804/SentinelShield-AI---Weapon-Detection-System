"""
Terminal-Based Weapon Detection
Run detection from command line with webcam or RTSP stream
No GUI required - Pure terminal interface
"""

import cv2
import sys
import time
from datetime import datetime
from pathlib import Path
import argparse

from detector import WeaponDetector
from alert_system import AlertSystem


class TerminalDetection:
    def __init__(self, source=0, confidence=0.90):
        """
        Initialize Terminal Detection
        
        Args:
            source: Camera index (0, 1, 2) or RTSP URL
            confidence: Detection confidence threshold (default: 0.90 for balanced strict detection)
        """
        self.source = source
        self.detector = WeaponDetector(confidence_threshold=confidence)
        self.alert_system = AlertSystem()
        self.running = False
        
        print("\n" + "="*60)
        print("SentinelShield AI - Weapon Detection System (Terminal Mode)")
        print("="*60)
        print(f"Source: {source}")
        print(f"Confidence Threshold: {confidence}")
        print(f"Device: {self.detector.device.upper()}")
        print("="*60 + "\n")
    
    def start(self):
        """Start detection"""
        # Open video source
        if isinstance(self.source, int):
            print(f"Opening webcam {self.source}...")
            cap = cv2.VideoCapture(self.source)
        else:
            print(f"Opening RTSP stream: {self.source}")
            cap = cv2.VideoCapture(self.source)
            # RTSP optimizations
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not cap.isOpened():
            print(f"❌ ERROR: Cannot open video source: {self.source}")
            return
        
        print("✓ Video source opened successfully!")
        print("\nControls:")
        print("  - Press 'q' to quit")
        print("  - Press 's' to save current frame")
        print("  - Detection window will show live feed\n")
        
        self.running = True
        frame_count = 0
        detection_count = 0
        start_time = time.time()
        
        try:
            while self.running:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ ERROR: Cannot read frame")
                    break
                
                frame_count += 1
                
                # Perform detection
                annotated_frame, detections, confidence_scores, has_detection = self.detector.detect(frame)
                
                # Handle detection
                if has_detection and detections:
                    detection_count += 1
                    
                    # Print to terminal
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\n[{timestamp}] ⚠️  WEAPON DETECTED!")
                    for det, conf in zip(detections, confidence_scores):
                        print(f"  - {det.upper()}: {conf:.2%}")
                    
                    # Trigger alert (save screenshot + sound)
                    alert_info = self.alert_system.trigger_alert(
                        annotated_frame, detections, confidence_scores
                    )
                    
                    if alert_info:
                        print(f"  ✓ Screenshot saved: {alert_info['screenshot']}")
                
                # Calculate and display FPS
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed
                    print(f"\r[FPS: {fps:.1f}] Frames: {frame_count} | Detections: {detection_count}", end="")
                
                # Show frame
                cv2.imshow('Weapon Detection - Press Q to quit', annotated_frame)
                
                # Check for key press
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n\nStopping detection...")
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"manual_save_{timestamp}.jpg"
                    cv2.imwrite(filename, annotated_frame)
                    print(f"\n✓ Frame saved: {filename}")
        
        except KeyboardInterrupt:
            print("\n\nDetection interrupted by user (Ctrl+C)")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            
            # Print summary
            elapsed = time.time() - start_time
            print("\n" + "="*60)
            print("Detection Summary")
            print("="*60)
            print(f"Total Frames: {frame_count}")
            print(f"Total Detections: {detection_count}")
            print(f"Total Alerts: {self.alert_system.get_alert_count()}")
            print(f"Runtime: {elapsed:.1f} seconds")
            print(f"Average FPS: {frame_count/elapsed:.1f}")
            print("="*60 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Terminal-based Weapon Detection System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default webcam (0)
  python terminal_detection.py
  
  # Use specific webcam
  python terminal_detection.py --source 1
  
  # Use RTSP stream
  python terminal_detection.py --source "rtsp://username:password@192.168.1.100:554/stream"
  
  # Adjust confidence threshold
  python terminal_detection.py --confidence 0.7
        """
    )
    
    parser.add_argument(
        '--source', '-s',
        default=0,
        help='Video source: webcam index (0, 1, 2) or RTSP URL (default: 0)'
    )
    
    parser.add_argument(
        '--confidence', '-c',
        type=float,
        default=0.90,
        help='Detection confidence threshold 0.0-1.0 (default: 0.90, balanced strict mode)'
    )
    
    args = parser.parse_args()
    
    # Convert source to int if it's a number
    try:
        source = int(args.source)
    except ValueError:
        source = args.source
    
    # Validate confidence
    if not 0.0 <= args.confidence <= 1.0:
        print("❌ ERROR: Confidence must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Start detection
    detector = TerminalDetection(source=source, confidence=args.confidence)
    detector.start()


if __name__ == "__main__":
    main()
