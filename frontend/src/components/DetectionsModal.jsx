import React from "react";

export default function DetectionsModal({ show, onClose, detections }) {
  if (!show) return null;

  return (
    <div className="modal d-block" tabIndex="-1" role="dialog" onClick={onClose}>
      <div
        className="modal-dialog modal-lg modal-dialog-centered"
        role="document"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Detections</h5>
            <button type="button" className="btn-close" aria-label="Close" onClick={onClose}></button>
          </div>

          <div className="modal-body">
            {detections && detections.length > 0 ? (
              <table className="table table-sm">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Person ID</th>
                    <th>Object</th>
                    <th>Gender</th>
                    <th>Emotion</th>
                    <th>Confidence</th>
                    <th>Box (x,y,w,h)</th>
                  </tr>
                </thead>
                <tbody>
                  {detections.map((d, i) => (
                    <tr key={d.id ?? i}>
                      <td>{i + 1}</td>
                      <td>{d.person_label || "-"}</td>
                      <td>{d.object_name}</td>
                      <td>{d.gender || "-"}</td>
                      <td>{d.emotion || "-"}</td>
                      <td>{typeof d.confidence === "number" ? `${(d.confidence * 100).toFixed(1)}%` : "-"}</td>
                      <td>{Array.isArray(d.box) ? d.box.join(", ") : "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="text-muted">No detections found.</div>
            )}
          </div>

          <div className="modal-footer">
            <button className="btn btn-secondary btn-sm" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}