from ultralytics import YOLO

def main():
    model = YOLO("yolov9s.pt")

    results = model.train(
        cfg="config.yaml"
    )
    results=model.val()

if __name__ == "__main__":
    main()