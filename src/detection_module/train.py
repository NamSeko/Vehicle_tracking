from ultralytics import YOLO

def main():
    model = YOLO("yolo_weights/yolov9s.pt")

    results = model.train(
        cfg="config.yaml"
    )
    results=model.val()

    success0 = model.export()
    success1 = model.export(format="onnx", dynamic=True, int8=True)
    success2 = model.export(format="engine", dynamic=True, int8=True)

if __name__ == "__main__":
    main()