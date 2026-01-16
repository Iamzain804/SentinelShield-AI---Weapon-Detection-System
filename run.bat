@echo off
echo ========================================
echo Hanif Jewellery - Weapon Detection System
echo ========================================
echo.

cd /d "%~dp0"

REM Check if custom model exists
if exist "models\weights\best.pt" (
    echo [INFO] Custom model found: models\weights\best.pt
    echo [INFO] Using your model for detection
) else (
    echo [WARNING] No custom model found at models\weights\best.pt
    echo [INFO] System will use base YOLOv8 model for testing
    echo.
    echo To use your own model:
    echo 1. Copy your .pt file to: models\weights\best.pt
    echo 2. Restart this application
    echo.
)

echo.
echo Starting GUI Application...
python src\gui_main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start application!
    echo Please run setup.bat first if you haven't already.
    pause
)
