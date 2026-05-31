import React from "react";

export default function Insights({ stats }) {
  return (
    <section id="insights">
      <h5 className="mb-3">Insights & Metrics</h5>

      <div className="row g-3">
        <div className="col-12 col-md-12">
          <div className="d-flex gap-2 flex-wrap">
            <div className="card flex-fill p-3">
              <small className="text-muted">Total Images Processed</small>
              <div className="h4 mb-0">{stats.processed ?? "—"}</div>
              <small className="text-muted">Last 30 days</small>
            </div>

            <div className="card flex-fill p-3">
              <small className="text-muted">Model Accuracy</small>
              <div className="h4 mb-0">{stats.accuracy ?? "—"}</div>
              <small className="text-muted">Measured on test sets</small>
            </div>

            <div className="card flex-fill p-3">
              <small className="text-muted">Avg Inference Time</small>
              <div className="h4 mb-0">{stats.time ?? "—"}</div>
              <small className="text-muted">per input</small>
            </div>
          </div>
        </div>
      </div>

      <div className="card mt-3 p-3" id="about">
        <h6 className="mb-2">Model breakdown</h6>
        <table className="table table-sm">
          <tbody>
            <tr>
              <td>Detection model</td>
              <td>{stats.detection_model || "YOLO"}</td>
              <td>Multi-object detection</td>
            </tr>
            <tr>
              <td>Face detector</td>
              <td>{stats.face_detector || "MTCNN"}</td>
              <td>Face crop extraction from persons</td>
            </tr>
            <tr>
              <td>Attribute model</td>
              <td>{stats.attribute_model || "EfficientNetV2-L"}</td>
              <td>Gender and emotion prediction</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="card mt-4 p-4">
        <h5 className="mb-3">About</h5>
        <p className="mb-0 text-muted">
          This web application demonstrates an Ensemble Deep Learning Framework for Multi Object Detection and Human Attribute Analysis.
          It supports image, video, and camera input, detects multiple objects, labels persons as P1, P2, P3, and predicts gender and emotion for human subjects.
        </p>
      </div>
    </section>
  );
}