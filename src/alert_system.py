"""
Alert System for Weapon Detection
Handles screenshot capture, alert notifications, and beep sounds
"""

import os
import cv2
import time
from datetime import datetime
from pathlib import Path
import threading
import logging
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    logger.warning("pygame not available, sound alerts disabled")


class AlertSystem:
    def __init__(self, alert_folder="alerts", sound_file="assets/alert.wav", cooldown=5):
        """
        Initialize Alert System with robust error handling
        
        Args:
            alert_folder: Folder to save alert screenshots
            sound_file: Path to alert sound file
            cooldown: Minimum seconds between alerts (must be >= 0)
        """
        # Validate cooldown
        if cooldown < 0:
            logger.warning(f"Invalid cooldown {cooldown}, using 5 seconds")
            cooldown = 5
        
        self.alert_folder = Path(alert_folder)
        try:
            self.alert_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"Alert folder: {self.alert_folder.absolute()}")
        except Exception as e:
            logger.error(f"Failed to create alert folder: {e}")
            # Fallback to current directory
            self.alert_folder = Path(".")
        
        self.sound_file = Path(sound_file)
        self.cooldown = cooldown
        self.last_alert_time = 0
        
        # Initialize pygame for sound with error handling
        self.sound = None
        if PYGAME_AVAILABLE:
            try:
                if self.sound_file.exists():
                    pygame.mixer.init()
                    self.sound = pygame.mixer.Sound(str(self.sound_file))
                    logger.info("✓ Sound system initialized")
                else:
                    logger.warning(f"Sound file not found at {self.sound_file}")
            except Exception as e:
                logger.error(f"Failed to initialize sound: {e}")
                self.sound = None
        
        self.alert_log = []
        self._lock = threading.Lock()  # Thread safety
    
    def can_alert(self):
        """Check if enough time has passed since last alert (thread-safe)"""
        with self._lock:
            current_time = time.time()
            if current_time - self.last_alert_time >= self.cooldown:
                return True
            return False
    
    def trigger_alert(self, frame, detections, confidence_scores):
        """
        Trigger alert: save screenshot, play sound, log event
        
        Args:
            frame: Current video frame (with bounding boxes drawn)
            detections: List of detected classes
            confidence_scores: List of confidence scores
        
        Returns:
            Alert info dict or None if cooldown active or error occurred
        """
        # Validate inputs
        if frame is None or not isinstance(frame, np.ndarray):
            logger.error("Invalid frame for alert")
            return None
        
        if frame.size == 0:
            logger.error("Empty frame for alert")
            return None
        
        if not detections:
            logger.warning("No detections provided for alert")
            return None
        
        # Check cooldown
        if not self.can_alert():
            return None
        
        try:
            # Update last alert time (thread-safe)
            with self._lock:
                self.last_alert_time = time.time()
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save screenshot with error handling
            screenshot_path = self.alert_folder / f"alert_{timestamp}.jpg"
            try:
                success = cv2.imwrite(str(screenshot_path), frame)
                if not success:
                    logger.error(f"Failed to save screenshot to {screenshot_path}")
                    screenshot_path = None
                else:
                    logger.info(f"✓ Screenshot saved: {screenshot_path}")
            except Exception as save_error:
                logger.error(f"Error saving screenshot: {save_error}")
                screenshot_path = None
            
            # Play alert sound in separate thread to avoid blocking
            if self.sound:
                try:
                    threading.Thread(target=self._play_sound, daemon=True).start()
                except Exception as sound_error:
                    logger.error(f"Error starting sound thread: {sound_error}")
            
            # Create alert info
            alert_info = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'detections': list(detections),  # Make a copy
                'confidence_scores': list(confidence_scores),  # Make a copy
                'screenshot': str(screenshot_path) if screenshot_path else None
            }
            
            # Add to log (thread-safe)
            with self._lock:
                self.alert_log.append(alert_info)
                
                # Keep only last 100 alerts in memory
                if len(self.alert_log) > 100:
                    self.alert_log = self.alert_log[-100:]
            
            return alert_info
            
        except Exception as e:
            logger.error(f"Error in trigger_alert: {e}")
            return None
    
    def _play_sound(self):
        """Play alert sound (runs in separate thread)"""
        try:
            if self.sound:
                self.sound.play()
        except Exception as e:
            logger.error(f"Error playing sound: {e}")
    
    def get_recent_alerts(self, count=10):
        """Get most recent alerts (thread-safe)"""
        with self._lock:
            return self.alert_log[-count:].copy() if self.alert_log else []
    
    def clear_alerts(self):
        """Clear alert log (thread-safe)"""
        with self._lock:
            self.alert_log = []
            logger.info("Alert log cleared")
    
    def get_alert_count(self):
        """Get total number of alerts (thread-safe)"""
        with self._lock:
            return len(self.alert_log)
