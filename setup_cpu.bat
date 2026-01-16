@echo off
echo ============================================================
echo Hanif Jewellery - Weapon Detection System Setup (CPU ONLY)
echo ============================================================
echo.

echo Installing CPU-only dependencies...
echo This will NOT install PyTorch/CUDA (GPU libraries)
echo.

pip install -r requirements_cpu.txt

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To run the system:
echo   python src\gui_main.py
echo.
echo Note: Running on CPU only (slower but works everywhere)
echo ============================================================
pause
