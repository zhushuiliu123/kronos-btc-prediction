#!/bin/bash
set -e

echo "============================================"
echo "  Kronos BTC Prediction Dashboard - Setup"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.10+ first."
    exit 1
fi

echo "[1/3] Installing dependencies..."
pip3 install -r requirements.txt -q
echo "      Done."

echo ""
echo "[2/3] Downloading model weights..."
python3 download_models.py
echo "      Done."

echo ""
echo "[3/3] Launching dashboard..."
echo ""
streamlit run kronos_dashboard.py
