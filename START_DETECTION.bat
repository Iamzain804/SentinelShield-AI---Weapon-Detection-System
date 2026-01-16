@echo off
echo ============================================================
echo SentinelShield AI - Weapon Detection (Quick Start)
echo ============================================================
echo.

REM Activate virtual environment and run terminal detection
echo Starting detection with webcam 0...
echo Press Q in the detection window to quit
echo.

cd /d "%~dp0src"
call env\Scripts\activate.bat
python terminal_detection.py --source 0

pause
