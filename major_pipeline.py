import os
import cv2
import torch
import timm
from PIL import Image
from torchvision import transforms
from ultralytics import YOLO
from facenet_pytorch import MTCNN
from collections import Counter, defaultdict
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

YOLO_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best.pt")
EMOTION_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "emotion_best.pth")
GENDER_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "gender_best.pth")

IMG_SIZE = 384
YOLO_CONF = 0.2
FRAME_SKIP = 2
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

EMOTION_CLASSES = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
GENDER_CLASSES = ['female', 'male']

OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUT_ROOT, exist_ok=True)


def build_model(num_classes):
    return timm.create_model(
        "tf_efficientnetv2_l.in21k",
        pretrained=False,
        num_classes=num_classes
    )


def load_model(model, path):
    ckpt = torch.load(path, map_location=DEVICE)
    model.load_state_dict(ckpt["model_state_dict"] if "model_state_dict" in ckpt else ckpt)
    model.to(DEVICE).eval()
    return model


def transform_image():
    return transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def predict(model, img, classes):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    x = transform_image()(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        out = model(x)
        prob = torch.softmax(out, dim=1)
        idx = torch.argmax(prob).item()

    return classes[idx], prob[0][idx].item()


def get_majority_label(counter_dict, default_value="unknown"):
    if not counter_dict:
        return default_value
    return max(counter_dict.items(), key=lambda x: x[1])[0]


def create_output_name(ext):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"processed_{ts}{ext}"


class MajorProjectAnalyzer:
    def __init__(self):
        self.yolo = YOLO(YOLO_MODEL_PATH)
        self.mtcnn = MTCNN(keep_all=False, device=DEVICE)
        self.emo_model = load_model(build_model(len(EMOTION_CLASSES)), EMOTION_MODEL_PATH)
        self.gen_model = load_model(build_model(len(GENDER_CLASSES)), GENDER_MODEL_PATH)

    def process_image_frame(self, frame):
        results = self.yolo(frame, conf=YOLO_CONF, verbose=False)[0]

        object_counter = Counter()
        person_details = []
        detections = []
        person_id = 1

        if results.boxes is not None:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                name = self.yolo.names[cls_id]
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)

                box_xywh = [x1, y1, x2 - x1, y2 - y1]

                if name == "person":
                    pid = f"P{person_id}"
                    gender = "unknown"
                    emotion = "unknown"
                    gender_conf = None
                    emotion_conf = None

                    crop = frame[y1:y2, x1:x2]

                    if crop.size != 0:
                        try:
                            face_boxes, _ = self.mtcnn.detect(
                                Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                            )

                            if face_boxes is not None and len(face_boxes) > 0:
                                fx1, fy1, fx2, fy2 = map(int, face_boxes[0])

                                fx1 = max(0, fx1)
                                fy1 = max(0, fy1)
                                fx2 = min(crop.shape[1], fx2)
                                fy2 = min(crop.shape[0], fy2)

                                face = crop[fy1:fy2, fx1:fx2]
                                if face.size != 0:
                                    emotion, emotion_conf = predict(self.emo_model, face, EMOTION_CLASSES)
                                    gender, gender_conf = predict(self.gen_model, face, GENDER_CLASSES)
                        except Exception:
                            pass

                    person_details.append({
                        "person_id": pid,
                        "gender": gender,
                        "emotion": emotion
                    })

                    detections.append({
                        "id": len(detections) + 1,
                        "person_label": pid,
                        "object_name": "person",
                        "box": box_xywh,
                        "confidence": conf,
                        "gender": gender,
                        "gender_confidence": gender_conf,
                        "emotion": emotion,
                        "emotion_confidence": emotion_conf
                    })

                    label = f"{pid} | {gender} | {emotion}"
                    color = (0, 255, 0)
                    person_id += 1

                else:
                    object_counter[name] += 1

                    detections.append({
                        "id": len(detections) + 1,
                        "person_label": None,
                        "object_name": name,
                        "box": box_xywh,
                        "confidence": conf,
                        "gender": None,
                        "gender_confidence": None,
                        "emotion": None,
                        "emotion_confidence": None
                    })

                    label = name
                    color = (0, 255, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        male_count = sum(1 for p in person_details if p["gender"] == "male")
        female_count = sum(1 for p in person_details if p["gender"] == "female")

        summary = {
            "persons_total": len(person_details),
            "male_count": male_count,
            "female_count": female_count,
            "person_details": person_details,
            "other_objects": dict(object_counter)
        }

        return frame, detections, summary

    def process_tracked_frame(self, frame, unique_persons, unique_objects, person_label_map):
        results = self.yolo.track(frame, conf=YOLO_CONF, persist=True, verbose=False)[0]
        frame_detections = []

        if results.boxes is None or len(results.boxes) == 0:
            return frame, frame_detections

        for box in results.boxes:
            cls_id = int(box.cls[0])
            name = self.yolo.names[cls_id]
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(frame.shape[1], x2)
            y2 = min(frame.shape[0], y2)

            box_xywh = [x1, y1, x2 - x1, y2 - y1]

            track_id = int(box.id[0]) if box.id is not None else None

            if name == "person":
                if track_id is None:
                    label = "person"
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, max(y1 - 10, 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    continue

                if track_id not in person_label_map:
                    person_label_map[track_id] = f"P{len(person_label_map) + 1}"

                display_id = person_label_map[track_id]

                if track_id not in unique_persons:
                    unique_persons[track_id] = {
                        "display_id": display_id,
                        "gender_votes": Counter(),
                        "emotion_votes": Counter(),
                        "last_gender": "unknown",
                        "last_emotion": "unknown"
                    }

                crop = frame[y1:y2, x1:x2]

                if crop.size != 0:
                    try:
                        face_boxes, _ = self.mtcnn.detect(
                            Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                        )

                        if face_boxes is not None and len(face_boxes) > 0:
                            fx1, fy1, fx2, fy2 = map(int, face_boxes[0])
                            fx1 = max(0, fx1)
                            fy1 = max(0, fy1)
                            fx2 = min(crop.shape[1], fx2)
                            fy2 = min(crop.shape[0], fy2)

                            face = crop[fy1:fy2, fx1:fx2]

                            if face.size != 0:
                                emotion, _ = predict(self.emo_model, face, EMOTION_CLASSES)
                                gender, _ = predict(self.gen_model, face, GENDER_CLASSES)

                                unique_persons[track_id]["gender_votes"][gender] += 1
                                unique_persons[track_id]["emotion_votes"][emotion] += 1
                                unique_persons[track_id]["last_gender"] = gender
                                unique_persons[track_id]["last_emotion"] = emotion
                    except Exception:
                        pass

                final_gender = unique_persons[track_id]["last_gender"]
                final_emotion = unique_persons[track_id]["last_emotion"]

                label = f"{display_id} | {final_gender} | {final_emotion}"
                color = (0, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                frame_detections.append({
                    "id": len(frame_detections) + 1,
                    "person_label": display_id,
                    "object_name": "person",
                    "box": box_xywh,
                    "confidence": conf,
                    "gender": final_gender,
                    "gender_confidence": None,
                    "emotion": final_emotion,
                    "emotion_confidence": None
                })

            else:
                if track_id is not None:
                    unique_objects[name].add(track_id)

                label = name
                color = (0, 255, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                frame_detections.append({
                    "id": len(frame_detections) + 1,
                    "person_label": None,
                    "object_name": name,
                    "box": box_xywh,
                    "confidence": conf,
                    "gender": None,
                    "gender_confidence": None,
                    "emotion": None,
                    "emotion_confidence": None
                })

        return frame, frame_detections

    def build_video_summary(self, unique_persons, unique_objects):
        final_persons = []

        for track_id, info in unique_persons.items():
            final_gender = get_majority_label(info["gender_votes"], "unknown")
            final_emotion = get_majority_label(info["emotion_votes"], "unknown")

            final_persons.append({
                "track_id": track_id,
                "person_id": info["display_id"],
                "gender": final_gender,
                "emotion": final_emotion
            })

        final_persons.sort(key=lambda x: int(x["person_id"][1:]))

        male_count = sum(1 for p in final_persons if p["gender"] == "male")
        female_count = sum(1 for p in final_persons if p["gender"] == "female")

        return {
            "persons_total": len(final_persons),
            "male_count": male_count,
            "female_count": female_count,
            "person_details": [
                {
                    "person_id": p["person_id"],
                    "gender": p["gender"],
                    "emotion": p["emotion"]
                }
                for p in final_persons
            ],
            "other_objects": {
                obj_name: len(obj_ids)
                for obj_name, obj_ids in unique_objects.items()
            }
        }

    def analyze_image(self, input_path):
        frame = cv2.imread(input_path)
        if frame is None:
            raise ValueError("Image not found or cannot be read")

        output_frame, detections, summary = self.process_image_frame(frame)

        output_filename = create_output_name(".jpg")
        output_path = os.path.join(OUTPUT_ROOT, output_filename)
        cv2.imwrite(output_path, output_frame)

        return {
            "mode": "image",
            "output_filename": output_filename,
            "detections": detections,
            "summary": summary
        }

    def analyze_video(self, input_path):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError("Video could not be opened")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 20.0

        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_filename = create_output_name(".mp4")
        output_path = os.path.join(OUTPUT_ROOT, output_filename)

        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (w, h)
        )

        unique_persons = {}
        unique_objects = defaultdict(set)
        person_label_map = {}

        frame_idx = 0
        last_detections = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % FRAME_SKIP == 0:
                output, frame_detections = self.process_tracked_frame(
                    frame.copy(),
                    unique_persons,
                    unique_objects,
                    person_label_map
                )
                last_detections = frame_detections
            else:
                output = frame.copy()

            out.write(output)
            frame_idx += 1

        cap.release()
        out.release()

        summary = self.build_video_summary(unique_persons, unique_objects)

        return {
            "mode": "video",
            "output_filename": output_filename,
            "detections": last_detections,
            "summary": summary
        }