import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Training LicensePlate Detection")
    parser.add_argument("--model", type=str, default="yolov9c.pt", help="YOLO model version like yolov9c.pt, yolo11s,...")
    parser.add_argument("--data", type=str, required=True, help="Path to your data file config (data.yaml)")
    parser.add_argument("--batch", type=int, default=32, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=512, help="Image size (e.g. 512)")
    parser.add_argument("--epochs", type=int, default=100, help="Epoch")
    parser.add_argument("--device", type=str, default="cuda", help="Epoch")

    args = parser.parse_args()
        
    model = YOLO(args.model)

    result = model.train(
        data = args.data,
        epochs = args.epochs,
        imgsz = args.imgsz,
        batch = args.batch,
        augment=True,
        device = args.device,
    )

    evaluation = model.eval()
    
if __name__ == "__main__":
    main()