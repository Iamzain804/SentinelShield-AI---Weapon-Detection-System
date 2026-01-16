@echo off
echo ============================================================
echo SentinelShield AI - Weapon Detection (Terminal Mode)
echo ============================================================
echo.

REM Check if virtual environment exists
if exist "src\env\Scripts\python.exe" (
    echo Using virtual environment...
    src\env\Scripts\python.exe src\terminal_detection.py %*
) else (
    echo Using system Python...
    python src\terminal_detection.py %*
)

echo.
echo ============================================================
echo Detection Stopped
echo ============================================================
pause
