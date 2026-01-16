# SentinelShield AI - Weapon Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-green)
![CUDA](https://img.shields.io/badge/CUDA-11.8-purple)
![License](https://img.shields.io/badge/License-MIT-orange)

**SentinelShield AI** is an advanced, real-time **Weapon Detection System** engineered for high-security environments. Leveraging the state-of-the-art **YOLOv8** object detection architecture, it delivers instantaneous threat identification from live video feeds (Webcam or RTSP) with exceptional accuracy. Designed for performance and reliability, SentinelShield AI integrates seamlessly into existing surveillance infrastructures to detect firearms, knives, and other threats.

---

## 🎯 Supported Weapons

SentinelShield AI is trained to detect and classify the following threats with high confidence:

*   **Pistols / Handguns**
*   **Knives / Bladed Weapons**
*   **Rifles / Long Guns**
*   *(Extendable to other classes with custom training)*

---

## 🚀 Key Features

*   **Instant Threat Detection**: Real-time analysis at 20-30 FPS with sub-100ms latency.
*   **Deep Learning Core**: Powered by YOLOv8 for precision detection of weapons (pistols, knives, etc.).
*   **Dual-Mode Operation**: Optimized for NVIDIA GPUs (CUDA) with robust CPU fallback.
*   **Tactical Dashboard**: A professional dark-themed GUI for centralized monitoring and control.
*   **Proactive Alerting**:
    *   **Visual**: Immediate on-screen threat highlighting.
    *   **Audible**: Distinctive alarm triggers upon detection.
    *   **Forensic Logging**: Automated high-res snapshots and event logging for post-incident review.
*   **Universal Compatibility**: Supports standard USB webcams and IP cameras via RTSP.

---

## 🛠️ System Architecture

SentinelShield AI is built on a high-performance, modular framework:

1.  **Command Center (GUI)**: The operational hub for monitoring and system configuration.
2.  **Video Stream Pipeline**: Multi-threaded capture engine handling diverse input sources.
3.  **Neural Inference Engine**: The brain of the system, executing YOLOv8 detection logic.
4.  **Sentinel Alert System**: Intelligent rule-based engine to manage alerts and prevent false positives.

---

## 📦 Installation

### Prerequisites
*   **OS**: Windows 10/11
*   **Python**: 3.8+
*   **Hardware**: NVIDIA GPU (RTX series recommended for optimal performance)

### Fast Track Setup
1.  **Clone the Repository**.
2.  **Initialize System**:
    Execute the automated setup script to install PyTorch, CUDA dependencies, and configure the environment.
    ```powershell
    .\setup.bat
    ```

---

## 🎮 Usage Instructions

1.  **Launch SentinelShield**:
    Start the application via the launcher script:
    ```powershell
    .\run.bat
    ```

2.  **Select Input Source**:
    *   Choose your camera device ID (0, 1, 2) from the interface.
    *   For IP Cameras, configure the RTSP URL in the settings.

3.  **Activate Monitoring**:
    *   Press **Start Detection** to engage the system.
    *   The feed will go live, overlaying bounding boxes and confidence scores on detected threats.

4.  **Incident Response**:
    *   **Snapshots**: Evidence is automatically saved to the `alerts/` directory.
    *   **Logs**: detailed event logs are maintained for security audits.

---

## 📂 Repository Structure

```text
SentinelShield/
├── src/
│   ├── gui_main.py       # Application Core
│   ├── detector.py       # Inference Engine
│   └── alert_system.py   # Event Handler
├── models/
│   └── weights/
│       └── best.pt       # Trained Model Weights
├── alerts/               # Incident Evidence
├── assets/               # System Resources
├── setup.bat             # Environment Configurator
├── run.bat               # System Launcher
└── requirements.txt      # Dependency Manifest
```

---

## 🔧 Troubleshooting

*   **GPU unavailable?**: Verify NVIDIA drivers and CUDA 11.8 installation.
*   **Camera feed black?**: Ensure no other background apps are monopolizing the video device.
*   **Startup failure?**: Re-run `setup.bat` to repair dependencies.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**SentinelShield AI Security Solutions**
