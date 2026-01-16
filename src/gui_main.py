"""
Hanif Jewellery - Weapon Detection Security System
Professional GUI Application with Real-time Detection
"""

import sys
import cv2
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QTextEdit, QGroupBox, QGridLayout, QFrame)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QPalette, QColor

from detector import WeaponDetector
from alert_system import AlertSystem


class VideoThread(QThread):
    """Thread for video capture and processing"""
    change_pixmap_signal = pyqtSignal(QImage)
    detection_signal = pyqtSignal(list, list, bool)
    fps_signal = pyqtSignal(float)
    
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        # High confidence (0.90) for balanced strict detection
        self.detector = WeaponDetector(confidence_threshold=0.90)
        self.cap = None
        
    def run(self):
        """Main video processing loop"""
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.running = True
        
        import time
        fps_start_time = time.time()
        fps_counter = 0
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Perform detection
                annotated_frame, detections, confidence_scores, has_detection = self.detector.detect(frame)
                
                # Convert to Qt format
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # Emit signals
                self.change_pixmap_signal.emit(qt_image)
                self.detection_signal.emit(detections, confidence_scores, has_detection)
                
                # Calculate FPS
                fps_counter += 1
                if fps_counter >= 30:
                    fps_end_time = time.time()
                    fps = fps_counter / (fps_end_time - fps_start_time)
                    self.fps_signal.emit(fps)
                    fps_counter = 0
                    fps_start_time = time.time()
        
        if self.cap:
            self.cap.release()
    
    def stop(self):
        """Stop video thread"""
        self.running = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SentinelShield AI - Weapon Detection System")
        self.setGeometry(100, 100, 1600, 900)
        
        # Set window icon
        icon_path = Path("assets/logo.webp")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Initialize components
        self.video_thread = None
        self.alert_system = AlertSystem()
        self.current_frame = None
        self.is_running = False
        
        # Setup UI
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Setup user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Left panel - Video feed
        left_panel = self.create_video_panel()
        main_layout.addWidget(left_panel, 7)
        
        # Right panel - Controls and info
        right_panel = self.create_control_panel()
        main_layout.addWidget(right_panel, 3)
        
    def create_video_panel(self):
        """Create video display panel"""
        panel = QGroupBox("Live Camera Feed")
        layout = QVBoxLayout(panel)
        
        # Video display
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(800, 600)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #1e293b;
                border: 3px solid #eb4c26;
                border-radius: 10px;
            }
        """)
        self.video_label.setText("Camera Not Started")
        layout.addWidget(self.video_label)
        
        # FPS and status bar
        status_layout = QHBoxLayout()
        
        self.fps_label = QLabel("FPS: 0")
        self.fps_label.setStyleSheet("color: #eb4c26; font-weight: bold; font-size: 14px;")
        status_layout.addWidget(self.fps_label)
        
        status_layout.addStretch()
        
        self.status_label = QLabel("● READY")
        self.status_label.setStyleSheet("color: #10b981; font-weight: bold; font-size: 14px;")
        status_layout.addWidget(self.status_label)
        
        layout.addLayout(status_layout)
        
        return panel
    
    def create_control_panel(self):
        """Create control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Title with SentinelShield AI logo
        title_layout = QHBoxLayout()
        
        # Logo
        icon_label = QLabel()
        icon_path = Path("assets/logo.webp")
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path)).scaled(150, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            title_layout.addWidget(icon_label)
        
        # Title Text
        title_label = QLabel("Weapon Detection")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #eb4c26;
            padding: 10px;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Camera selection
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QVBoxLayout(camera_group)
        
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(["Webcam 0", "Webcam 1", "Webcam 2"])
        camera_layout.addWidget(QLabel("Select Camera:"))
        camera_layout.addWidget(self.camera_combo)
        
        layout.addWidget(camera_group)
        
        # Control buttons
        control_group = QGroupBox("Controls")
        control_layout = QVBoxLayout(control_group)
        
        self.start_btn = QPushButton("▶ Start Detection")
        self.start_btn.clicked.connect(self.start_detection)
        self.start_btn.setMinimumHeight(50)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Detection")
        self.stop_btn.clicked.connect(self.stop_detection)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(50)
        control_layout.addWidget(self.stop_btn)
        
        layout.addWidget(control_group)
        
        # Detection info
        detection_group = QGroupBox("Detection Information")
        detection_layout = QVBoxLayout(detection_group)
        
        self.detection_label = QLabel("No detections")
        self.detection_label.setWordWrap(True)
        self.detection_label.setStyleSheet("font-size: 12px; padding: 10px;")
        detection_layout.addWidget(self.detection_label)
        
        layout.addWidget(detection_group)
        
        # Statistics
        stats_group = QGroupBox("Statistics")
        stats_layout = QGridLayout(stats_group)
        
        stats_layout.addWidget(QLabel("Total Alerts:"), 0, 0)
        self.total_alerts_label = QLabel("0")
        self.total_alerts_label.setStyleSheet("font-weight: bold; color: #ef4444;")
        stats_layout.addWidget(self.total_alerts_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Mode:"), 1, 0)
        self.gpu_label = QLabel("CPU Only")
        self.gpu_label.setStyleSheet("font-weight: bold; color: #10b981;")
        stats_layout.addWidget(self.gpu_label, 1, 1)
        
        layout.addWidget(stats_group)
        
        # Alert log
        log_group = QGroupBox("Alert Log")
        log_layout = QVBoxLayout(log_group)
        
        self.alert_log = QTextEdit()
        self.alert_log.setReadOnly(True)
        self.alert_log.setMaximumHeight(200)
        log_layout.addWidget(self.alert_log)
        
        layout.addWidget(log_group)
        
        # Footer
        footer_label = QLabel("Powered by SentinelShield AI")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #eb4c26; font-size: 10px; font-weight: bold;")
        layout.addWidget(footer_label)
        
        return panel
    
    def apply_styles(self):
        """Apply custom styles with SentinelShield Orange Theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QGroupBox {
                background-color: #1e293b;
                border: 2px solid #eb4c26;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
                color: #eb4c26;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #eb4c26;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f28325;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #475569;
                color: #94a3b8;
            }
            QComboBox {
                background-color: #1e293b;
                color: white;
                border: 2px solid #eb4c26;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #e2e8f0;
            }
            QTextEdit {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 2px solid #eb4c26;
                border-radius: 5px;
                padding: 5px;
            }
        """)
    
    def start_detection(self):
        """Start video detection"""
        camera_index = self.camera_combo.currentIndex()
        
        self.video_thread = VideoThread(camera_index)
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.detection_signal.connect(self.handle_detection)
        self.video_thread.fps_signal.connect(self.update_fps)
        self.video_thread.start()
        
        self.is_running = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.camera_combo.setEnabled(False)
        self.status_label.setText("● MONITORING")
        self.status_label.setStyleSheet("color: #10b981; font-weight: bold; font-size: 14px;")
        
    def stop_detection(self):
        """Stop video detection"""
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread = None
        
        self.is_running = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.camera_combo.setEnabled(True)
        self.status_label.setText("● STOPPED")
        self.status_label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
        self.video_label.setText("Camera Stopped")
        
    def update_image(self, qt_image):
        """Update video display"""
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(scaled_pixmap)
        
        # Store current frame for alerts
        self.current_frame = qt_image
        
    def update_fps(self, fps):
        """Update FPS display"""
        self.fps_label.setText(f"FPS: {fps:.1f}")
        
    def handle_detection(self, detections, confidence_scores, has_detection):
        """Handle detection results"""
        if has_detection and detections:
            # Update detection info
            detection_text = ""
            for det, conf in zip(detections, confidence_scores):
                detection_text += f"⚠ {det.upper()}: {conf:.2%}\n"
            
            self.detection_label.setText(detection_text)
            self.detection_label.setStyleSheet("font-size: 12px; padding: 10px; color: #ef4444; font-weight: bold;")
            
            # Trigger alert
            if self.current_frame and self.video_thread:
                # Convert QImage back to numpy array for alert system
                import numpy as np
                width = self.current_frame.width()
                height = self.current_frame.height()
                ptr = self.current_frame.bits()
                ptr.setsize(height * width * 3)
                arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 3))
                frame_bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
                
                alert_info = self.alert_system.trigger_alert(frame_bgr, detections, confidence_scores)
                
                if alert_info:
                    # Update alert log
                    log_entry = f"[{alert_info['timestamp']}] ALERT: {', '.join(alert_info['detections'])}\n"
                    self.alert_log.append(log_entry)
                    
                    # Update stats
                    self.total_alerts_label.setText(str(self.alert_system.get_alert_count()))
                    
                    # Change status
                    self.status_label.setText("● ALERT!")
                    self.status_label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
        else:
            self.detection_label.setText("No detections")
            self.detection_label.setStyleSheet("font-size: 12px; padding: 10px; color: #10b981;")
            
            if self.is_running:
                self.status_label.setText("● MONITORING")
                self.status_label.setStyleSheet("color: #10b981; font-weight: bold; font-size: 14px;")
    
    def closeEvent(self, event):
        """Handle window close"""
        self.stop_detection()
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
