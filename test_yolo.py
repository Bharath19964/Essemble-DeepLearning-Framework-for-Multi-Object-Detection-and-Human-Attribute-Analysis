import cv2
from ultralytics import YOLO

# ---------------- CONFIG ----------------
MODEL_PATH = r"models/best.pt"
INPUT_PATH = r"test inputs/video 1.mp4"   # can also be video file
CONF = 0.2
# ----------------------------------------

def run_yolo_test():
    model = YOLO(MODEL_PATH)

    results = model.predict(
        source=INPUT_PATH,
        conf=CONF,
        save=False,
        show=False
    )

    for result in results:
        annotated = result.plot()

        cv2.imshow("YOLO Detection", annotated)
        print("Detected objects:")

        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                class_name = model.names[cls_id]
                xyxy = box.xyxy[0].tolist()

                print(f"Class: {class_name}, Confidence: {conf:.2f}, Box: {xyxy}")

        cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_yolo_test()