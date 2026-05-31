// frontend/src/components/Gallery.jsx
import React from "react";

export default function Gallery({ samples, onUse }) {
  return (
    <section id="tests" className="mb-4">
      <h5 className="mb-3">Test Images</h5>
      <div className="row g-3">
        {samples.map((img) => (
          <div key={img.id} className="col-sm-6 col-md-4">
            <div className="card h-100 shadow-sm">
              <div style={{ height: 180, overflow: "hidden" }}>
                <img
                  src={img.src}
                  className="card-img-top"
                  alt={img.name}
                  style={{ objectFit: "cover", width: "100%", height: "250px" }}
                  onError={(e) => {
                    console.error("Image failed to load:", img.src);
                    e.target.src = "/images/fallback.png"; // optional fallback image placed in public/images
                    e.target.style.objectFit = "contain";
                  }}
                />
              </div>
              <div className="card-body d-flex flex-column">
                <h6 className="card-title mb-2">{img.name}</h6>
                <div className="mt-auto d-flex justify-content-end">
                  <button className="btn btn-sm btn-primary me-2" onClick={() => onUse(img)}>
                    Use
                  </button>
                  <button className="btn btn-sm btn-outline-secondary" onClick={() => window.open(img.src, "_blank")}>
                    Open
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
