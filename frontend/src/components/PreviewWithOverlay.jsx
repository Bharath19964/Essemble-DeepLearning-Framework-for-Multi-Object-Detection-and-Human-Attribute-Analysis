import React, { useRef } from "react";

export default function PreviewWithOverlay({ src, detections }) {
  const imgRef = useRef(null);

  return (
    <div style={{ position: "relative" }} className="border rounded overflow-hidden bg-light">
      {src ? (
        <>
          <img
            ref={imgRef}
            src={src}
            alt="preview"
            style={{ width: "100%", display: "block", height: "auto" }}
          />

          <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
            {detections &&
              detections.map((d) => {
                const [x, y, w, h] = d.box;
                const imgEl = imgRef.current;
                if (!imgEl || !imgEl.naturalWidth) return null;

                const displayWidth = imgEl.clientWidth;
                const displayHeight = imgEl.clientHeight;
                const scaleX = displayWidth / imgEl.naturalWidth;
                const scaleY = displayHeight / imgEl.naturalHeight;

                const left = x * scaleX;
                const top = y * scaleY;
                const width = w * scaleX;
                const height = h * scaleY;

                const isPerson = d.object_name === "person";
                const label = isPerson
                  ? `${d.person_label || "P"} | ${d.gender || "unknown"} | ${d.emotion || "unknown"}`
                  : d.object_name;

                return (
                  <div
                    key={d.id}
                    style={{
                      position: "absolute",
                      left,
                      top,
                      width,
                      height,
                      border: isPerson
                        ? "2px solid rgba(0,123,255,0.95)"
                        : "2px solid rgba(40,167,69,0.95)",
                      boxSizing: "border-box",
                      borderRadius: 6,
                    }}
                  >
                    <div
                      style={{
                        background: isPerson
                          ? "rgba(0,123,255,0.95)"
                          : "rgba(40,167,69,0.95)",
                        color: "#fff",
                        fontSize: 12,
                        padding: "2px 6px",
                        borderTopLeftRadius: 6,
                        display: "inline-block",
                      }}
                    >
                      {label}
                    </div>
                  </div>
                );
              })}
          </div>
        </>
      ) : (
        <div className="p-4 text-center text-muted">No image selected</div>
      )}
    </div>
  );
}