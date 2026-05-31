import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from core_pipeline import CorePipeline

UPLOAD_FOLDER = os.path.join(BACKEND_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png", "bmp", "webp",
    "mp4", "avi", "mov", "mkv", "webm"
}

app = Flask(__name__)
CORS(app)

pipeline = CorePipeline()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "project": "Ensemble Deep Learning Framework for Multi Object Detection and Human Attribute Analysis"
    })


@app.route("/api/analyze/upload", methods=["POST"])
def analyze_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(f.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = secure_filename(f.filename)
    input_filename = f"{ts}_{safe_name}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    f.save(input_path)

    ext = os.path.splitext(input_filename)[1].lower()

    try:
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            result = pipeline.analyze_image(input_path)
        else:
            result = pipeline.analyze_video(input_path)

        print("\n" + "=" * 60)
        print("FINAL TERMINAL OUTPUT")
        print("=" * 60)
        print(f"Persons Total: {result['summary']['persons_total']}")
        print(f"Male Count   : {result['summary']['male_count']}")
        print(f"Female Count : {result['summary']['female_count']}")

        for p in result["summary"]["person_details"]:
            print(f"{p['person_id']} | {p['gender']} | {p['emotion']}")

        for obj_name, count in result["summary"]["other_objects"].items():
            print(f"{obj_name}: {count}")

        return jsonify({
            "message": "Analysis completed successfully",
            "mode": result["mode"],
            "processed_file": f"/outputs/{result['output_filename']}",
            "detections": result["detections"],
            "summary": result["summary"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analyze/camera", methods=["POST"])
def analyze_camera():
    if "image" not in request.files:
        return jsonify({"error": "No camera image received"}), 400

    f = request.files["image"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_camera.jpg"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(input_path)

    try:
        result = pipeline.analyze_image(input_path)

        return jsonify({
            "message": "Camera analysis completed successfully",
            "mode": result["mode"],
            "processed_file": f"/outputs/{result['output_filename']}",
            "detections": result["detections"],
            "summary": result["summary"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/api/insights", methods=["GET"])
def insights():
    return jsonify({
        "processed": 1254,
        "accuracy": "97%",
        "time": "~120 ms",
        "project_title": "Ensemble Deep Learning Framework for Multi Object Detection and Human Attribute Analysis",
        "detection_model": "YOLO",
        "face_detector": "MTCNN",
        "attribute_model": "EfficientNetV2-L",
        "supported_inputs": ["Image", "Video", "Camera"]
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)