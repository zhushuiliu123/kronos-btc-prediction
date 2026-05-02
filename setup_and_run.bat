@echo off
chcp 65001 >nul
echo ============================================
echo   Kronos BTC Prediction Dashboard - Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+ first.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo       Done.

echo.
echo [2/3] Downloading model weights...
python download_models.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to download model weights.
    pause
    exit /b 1
)
echo       Done.

echo.
echo [3/3] Launching dashboard...
echo.
streamlit run kronos_dashboard.py
