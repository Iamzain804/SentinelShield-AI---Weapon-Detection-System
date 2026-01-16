@echo off
echo ========================================
echo Hanif Jewellery - Weapon Detection Setup
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo.

echo Step 2: Installing PyTorch with CUDA support...
echo This may take several minutes...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
echo.

echo Step 3: Installing other dependencies...
pip install -r requirements.txt
echo.

echo Step 4: Verifying GPU...
python -c "import torch; print('GPU Available:', torch.cuda.is_available()); print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   python src\gui_main.py
echo.
pause
