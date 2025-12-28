#!/bin/bash
# setup_gptsovits.sh
# Runs the internal download.py to fetch pretrained models for GPT-SoVITS

echo "--- Setting up GPT-SoVITS Models ---"

# 1. Check if we are in the right place
DOWNLOAD_SCRIPT="download_models.py"

if [ ! -f "$DOWNLOAD_SCRIPT" ]; then
    echo "❌ Could not find $DOWNLOAD_SCRIPT in current directory."
    echo "Please run this script from the repo root inside the container."
    exit 1
fi

echo "Found downloader: $DOWNLOAD_SCRIPT"
echo "Running custom download script..."

python "$DOWNLOAD_SCRIPT"

echo "Checking pretrained_models..."
ls -R /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models
