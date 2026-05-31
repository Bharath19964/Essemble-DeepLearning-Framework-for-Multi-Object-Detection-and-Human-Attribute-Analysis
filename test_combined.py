import os
import cv2
from core_pipeline import CorePipeline, create_output_dirs

# ================= CONFIG =================
INPUT_SOURCE = 0
# image path example:
# INPUT_SOURCE = r"test inputs\img1.jpg"
# video path example:
# INPUT_SOURCE = r"test inputs\video1.mp4"
# webcam:
# INPUT_SOURCE = 0
# ==========================================


def print_image_summary(summary):
    print("\n===== IMAGE SUMMARY =====")
    print(f"Persons: {summary['persons_total']}")
    print(f"Male: {summary['male_count']}")
    print(f"Female: {summary['female_count']}")

    for p in summary["person_details"]:
        print(f"{p['person_id']} | {p['gender']} | {p['emotion']}")

    for k, v in summary["other_objects"].items():
        print(f"{k}: {v}")


def print_video_summary(summary):
    print("\n===== WHOLE VIDEO SUMMARY =====")
    print(f"Persons: {summary['persons_total']}")
    print(f"Male: {summary['male_count']}")
    print(f"Female: {summary['female_count']}")

    for p in summary["person_details"]:
        print(f"{p['person_id']} | {p['gender']} | {p['emotion']}")

    for k, v in summary["other_objects"].items():
        print(f"{k}: {v}")


def run_image_mode(pipeline, image_path):
    result = pipeline.analyze_image(image_path)
    print_image_summary(result["summary"])

    output = cv2.imread(result["output_path"])
    if output is not None:
        cv2.imshow("Output", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print("\nSaved Image:", result["output_path"])


def run_video_mode(pipeline, video_path):
    result = pipeline.analyze_video(video_path)
    print_video_summary(result["summary"])
    print("\nSaved Video:", result["output_path"])


def run_webcam_mode():
    pipeline = CorePipeline()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ValueError("Webcam could not be opened")

    print("\nWEBCAM CONTROLS:")
    print("Press 'C' -> Capture image and analyze")
    print("Press 'R' -> Start/Stop recording raw webcam video")
    print("Press 'ESC' -> Exit")

    save_dir = create_output_dirs()
    recording = False
    out = None
    raw_video_path = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam", frame)
        if recording and out is not None:
            out.write(frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

        elif key == ord('c'):
            img_path = os.path.join(save_dir, f"capture_{frame_idx}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"\nCaptured Image: {img_path}")
            result = pipeline.analyze_image(img_path)
            print_image_summary(result["summary"])
            print("Processed Image:", result["output_path"])

        elif key == ord('r'):
            if not recording:
                h, w = frame.shape[:2]
                raw_video_path = os.path.join(save_dir, "webcam_raw.mp4")
                out = cv2.VideoWriter(
                    raw_video_path,
                    cv2.VideoWriter_fourcc(*"mp4v"),
                    20.0,
                    (w, h)
                )
                recording = True
                print("\nRecording started...")
            else:
                recording = False
                if out is not None:
                    out.release()
                    out = None
                print("\nRecording stopped.")
                print("Raw Video Saved:", raw_video_path)

                if raw_video_path and os.path.exists(raw_video_path):
                    result = pipeline.analyze_video(raw_video_path)
                    print_video_summary(result["summary"])
                    print("Processed Video:", result["output_path"])

        frame_idx += 1

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()


def main():
    print("Running with shared core_pipeline.py")

    pipeline = CorePipeline()

    if INPUT_SOURCE == 0:
        run_webcam_mode()

    elif isinstance(INPUT_SOURCE, str) and os.path.isfile(INPUT_SOURCE):
        ext = os.path.splitext(INPUT_SOURCE)[1].lower()

        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            run_image_mode(pipeline, INPUT_SOURCE)
        else:
            run_video_mode(pipeline, INPUT_SOURCE)

    else:
        raise ValueError("Invalid INPUT_SOURCE")


if __name__ == "__main__":
    main()