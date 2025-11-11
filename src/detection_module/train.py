from ultralytics import YOLO

def main():
    model = YOLO("yolo_weights/yolov9s.pt")

    results = model.train(
        cfg="config.yaml"
    )
    results=model.val()

    success0 = model.export()

if __name__ == "__main__":
    main()