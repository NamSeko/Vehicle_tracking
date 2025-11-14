#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$LOCAL_DIR/VehicleDetection"
cd $PROJECT_DIR

# Download data if you don't have.
pip install gdown
!gdown "1w03UuNfQBP0Rt0Fgp-l4thHfGKmuhHWS"
!gdown "1555uoeRfFPMMWmGobSx-ZhgdR3Q-7zQi"

# Unzip data
sudo apt-get install unzip
unzip dataset.zip -d data

python src/train/train.py \
    --model "yolov9c.pt" \
    --data "trafics_data.yaml" \
    --batch 32 \
    --imgsz 512 \
    --epochs 100 \
    --device "cuda"