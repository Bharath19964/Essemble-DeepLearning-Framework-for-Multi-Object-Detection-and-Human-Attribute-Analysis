import React from "react";

export default function Hero({
  onUpload,
  onOpenCamera,
  onAnalyze,
  onCaptureAnalyze,
  onOpenDetections,
  onStartRecording,
  onStopRecording,
  onAnalyzeRecordedVideo,
  loading,
  detections,
  summary,
  selectedFile,
  cameraOpen,
  isRecording,
  recordedVideoReady,
}) {
  return (
    <section className="card mb-4 shadow-sm hero-main-card">
      <div className="card-body">
        <div className="row align-items-start">
          <div className="col-md-8">
            <h2 className="hero-heading">
              Multi Object Detection & Human Attribute Analysis
            </h2>

            <p className="text-muted mb-3 hero-subtext">
              Upload an image or video or use your camera. Backend: YOLO + MTCNN + EfficientNetV2-L.
            </p>

            <div className="d-flex flex-wrap gap-2 align-items-center">
              <label className="btn btn-outline-secondary btn-sm mb-1">
                Choose Image / Video
                <input
                  type="file"
                  accept="image/*,video/*"
                  hidden
                  onChange={(e) => onUpload(e.target.files && e.target.files[0])}
                />
              </label>

              <button className="btn btn-outline-primary btn-sm mb-1" onClick={onOpenCamera}>
                Open Camera
              </button>

              <button
                className="btn btn-success btn-sm mb-1"
                onClick={onAnalyze}
                disabled={loading || cameraOpen || !selectedFile}
              >
                {loading ? "Analyzing..." : "Analyze"}
              </button>

              <button
                className="btn btn-outline-dark btn-sm mb-1"
                onClick={onCaptureAnalyze}
                disabled={loading || !cameraOpen}
              >
                Capture Image
              </button>

              <button
                className="btn btn-outline-danger btn-sm mb-1"
                onClick={onStartRecording}
                disabled={loading || !cameraOpen || isRecording}
              >
                Start Recording
              </button>

              <button
                className="btn btn-danger btn-sm mb-1"
                onClick={onStopRecording}
                disabled={loading || !cameraOpen || !isRecording}
              >
                Stop Recording
              </button>

              <button
                className="btn btn-warning btn-sm mb-1"
                onClick={onAnalyzeRecordedVideo}
                disabled={loading || !recordedVideoReady}
              >
                Analyze Recorded Video
              </button>

              <button
                className="btn btn-outline-info btn-sm mb-1"
                onClick={onOpenDetections}
                disabled={!detections || detections.length === 0}
              >
                View Detections
              </button>
            </div>

            <div className="text-muted small mt-3">
              Model Info: YOLO for multi-object detection · MTCNN for face detection · EfficientNetV2-L for gender and emotion
            </div>

            <div className="mt-4">
              <h6 className="fw-bold mb-2">Counts:</h6>
              <div className="d-flex flex-wrap gap-2">
                <span className="badge rounded-pill bg-secondary px-3 py-2">
                  Total: {summary?.persons_total ?? 0}
                </span>
                <span className="badge rounded-pill bg-primary px-3 py-2">
                  Male: {summary?.male_count ?? 0}
                </span>
                <span className="badge rounded-pill bg-danger px-3 py-2">
                  Female: {summary?.female_count ?? 0}
                </span>
              </div>
            </div>
          </div>

          <div className="col-md-4">
            <div className="mini-pipeline-box">
              <h6 className="fw-bold mb-2">Pipeline</h6>
              <ul className="mb-0 small">
                <li>YOLO object detection</li>
                <li>MTCNN face extraction</li>
                <li>EfficientNetV2-L gender</li>
                <li>EfficientNetV2-L emotion</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}