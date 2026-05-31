import React from "react";

export default function ResultsPanel({ summary, detections }) {
  return (
    <div className="card shadow-sm mt-4">
      <div className="card-body">
        <h5 className="mb-3">Analysis Output</h5>

        {!summary ? (
          <div className="text-muted">No analysis output yet.</div>
        ) : (
          <>
            <div className="row g-3 mb-4">
              <div className="col-md-4">
                <div className="card p-3 h-100">
                  <small className="text-muted">Persons Total</small>
                  <div className="h3 mb-0">{summary.persons_total}</div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card p-3 h-100">
                  <small className="text-muted">Male Count</small>
                  <div className="h3 mb-0 text-primary">{summary.male_count}</div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="card p-3 h-100">
                  <small className="text-muted">Female Count</small>
                  <div className="h3 mb-0 text-danger">{summary.female_count}</div>
                </div>
              </div>
            </div>

            <h6 className="mb-2">Person Details</h6>
            {summary.person_details && summary.person_details.length > 0 ? (
              <table className="table table-sm mb-4">
                <thead>
                  <tr>
                    <th>Person ID</th>
                    <th>Gender</th>
                    <th>Emotion</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.person_details.map((p, i) => (
                    <tr key={i}>
                      <td>{p.person_id}</td>
                      <td>{p.gender}</td>
                      <td>{p.emotion}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="text-muted mb-4">No persons detected.</div>
            )}

            <h6 className="mb-2">Other Object Class-wise Count</h6>
            {summary.other_objects && Object.keys(summary.other_objects).length > 0 ? (
              <div className="row g-2">
                {Object.entries(summary.other_objects).map(([name, count]) => (
                  <div className="col-md-3 col-sm-4 col-6" key={name}>
                    <div className="border rounded p-2 d-flex justify-content-between align-items-center bg-light">
                      <span className="text-capitalize">{name}</span>
                      <strong>{count}</strong>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-muted">No other objects detected.</div>
            )}

            <div className="mt-4 small text-muted">
              Returned detections: {detections?.length || 0}
            </div>
          </>
        )}
      </div>
    </div>
  );
}