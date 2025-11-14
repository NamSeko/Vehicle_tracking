#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$LOCAL_DIR/LicensePlate"
cd $PROJECT_DIR

# Download data if you don't have.
pip install gdown
!gdown "13PChAtrnopdVB6mQOY1tHQXULJIRTWe6"

# Unzip data
sudo apt-get install unzip
unzip License_Plate_Augment.zip -d data

python src/train/train.py \
    --model "yolov9c.pt" \
    --data "$PROJECT_DIR/data/data.yaml" \
    --batch 32 \
    --imgsz 512 \
    --epochs 100 \
    --device "cuda"