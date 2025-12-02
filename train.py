from ultralytics import YOLO

def main():
    model = YOLO("./runs/detect/train/weights/last.pt")
    model.train(data="data.yaml", epochs=40, resume=True)
    metrics = model.val()

if __name__ == '__main__':
    main()