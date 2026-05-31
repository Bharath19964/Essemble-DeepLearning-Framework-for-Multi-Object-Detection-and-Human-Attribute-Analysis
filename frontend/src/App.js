import React, { useEffect, useRef, useState } from "react";
import Header from "./components/Header";
import Hero from "./components/Hero";
import PreviewWithOverlay from "./components/PreviewWithOverlay";
import DetectionsModal from "./components/DetectionsModal";
import Insights from "./components/Insights";
import ResultsPanel from "./components/ResultsPanel";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewSrc, setPreviewSrc] = useState("");
  const [processedSrc, setProcessedSrc] = useState("");
  const [detections, setDetections] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showDetections, setShowDetections] = useState(false);
  const [stats, setStats] = useState({});
  const [mode, setMode] = useState("");

  const [cameraOpen, setCameraOpen] = useState(false);
  const [cameraReady, setCameraReady] = useState(false);

  const [isRecording, setIsRecording] = useState(false);
  const [recordedVideoBlob, setRecordedVideoBlob] = useState(null);
  const [recordedVideoUrl, setRecordedVideoUrl] = useState("");

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/insights`)
      .then((r) => r.json())
      .then((data) => setStats(data))
      .catch(() => {});
  }, []);

  const resetOutputs = () => {
    setProcessedSrc("");
    setDetections([]);
    setSummary(null);
  };

  const handleUpload = (file) => {
    if (!file) return;

    stopCamera();

    setSelectedFile(file);
    resetOutputs();
    setMode(file.type?.startsWith("video/") ? "video" : "image");

    const localUrl = URL.createObjectURL(file);
    setPreviewSrc(localUrl);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert("Please choose an image or video first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/analyze/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Analysis failed");

      setProcessedSrc(`${API_BASE}${data.processed_file}?t=${Date.now()}`);
      setDetections(data.detections || []);
      setSummary(data.summary || null);
      setMode(data.mode || "");
    } catch (err) {
      console.error(err);
      alert(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const openCamera = async () => {
    try {
      stopCamera();

      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });

      streamRef.current = stream;
      setCameraOpen(true);
      setCameraReady(false);
      setSelectedFile(null);
      setRecordedVideoBlob(null);
      setRecordedVideoUrl("");
      resetOutputs();
      setMode("camera");

      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
          setCameraReady(true);
        }
      }, 150);
    } catch (err) {
      console.error(err);
      alert("Unable to access camera.");
    }
  };

  const stopCamera = () => {
    if (isRecording) {
      stopRecording();
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setCameraOpen(false);
    setCameraReady(false);
  };

  const captureAndAnalyzeImage = async () => {
    if (!videoRef.current || !canvasRef.current) {
      alert("Camera is not ready.");
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const previewUrl = canvas.toDataURL("image/jpeg");
      setPreviewSrc(previewUrl);

      const formData = new FormData();
      formData.append("image", blob, "camera_capture.jpg");

      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/api/analyze/camera`, {
          method: "POST",
          body: formData,
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Camera image analysis failed");

        setProcessedSrc(`${API_BASE}${data.processed_file}`);
        setDetections(data.detections || []);
        setSummary(data.summary || null);
        setMode(data.mode || "image");
      } catch (err) {
        console.error(err);
        alert(err.message || "Camera image analysis failed");
      } finally {
        setLoading(false);
      }
    }, "image/jpeg", 0.95);
  };

  const startRecording = () => {
    if (!streamRef.current) {
      alert("Open camera first.");
      return;
    }

    recordedChunksRef.current = [];
    setRecordedVideoBlob(null);
    setRecordedVideoUrl("");
    resetOutputs();

    const mimeType = MediaRecorder.isTypeSupported("video/webm;codecs=vp8,opus")
      ? "video/webm;codecs=vp8,opus"
      : "video/webm";

    const mediaRecorder = new MediaRecorder(streamRef.current, { mimeType });

    mediaRecorder.ondataavailable = (event) => {
      if (event.data && event.data.size > 0) {
        recordedChunksRef.current.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunksRef.current, { type: "video/webm" });
      const url = URL.createObjectURL(blob);

      setRecordedVideoBlob(blob);
      setRecordedVideoUrl(url);
      setPreviewSrc(url);
      setSelectedFile(null);
      setMode("video");
    };

    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  const analyzeRecordedVideo = async () => {
    if (!recordedVideoBlob) {
      alert("No recorded video found. Record and stop first.");
      return;
    }

    const file = new File([recordedVideoBlob], "camera_recording.webm", {
      type: "video/webm",
    });

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/analyze/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Recorded video analysis failed");

      setProcessedSrc(`${API_BASE}${data.processed_file}`);
      setDetections(data.detections || []);
      setSummary(data.summary || null);
      setMode(data.mode || "video");
    } catch (err) {
      console.error(err);
      alert(err.message || "Recorded video analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Header />

      <main className="container py-4">
        <Hero
          onUpload={handleUpload}
          onOpenCamera={openCamera}
          onAnalyze={handleAnalyze}
          onCaptureAnalyze={captureAndAnalyzeImage}
          onOpenDetections={() => setShowDetections(true)}
          onStartRecording={startRecording}
          onStopRecording={stopRecording}
          onAnalyzeRecordedVideo={analyzeRecordedVideo}
          loading={loading}
          detections={detections}
          summary={summary}
          selectedFile={selectedFile}
          cameraOpen={cameraOpen}
          isRecording={isRecording}
          recordedVideoReady={!!recordedVideoBlob}
        />

        <div className="row g-4">
          <div className="col-lg-7">
            <div className="card app-card shadow-sm">
              <div className="card-body">
                <h4 className="section-title">Input Preview</h4>

                {cameraOpen ? (
                  <div className="preview-wrap">
                    <video
                      ref={videoRef}
                      autoPlay
                      muted
                      playsInline
                      className="plain-preview"
                    />
                    {!cameraReady && (
                      <div className="camera-note">Opening camera...</div>
                    )}

                    <button
                      className="btn btn-sm btn-outline-danger mt-3"
                      onClick={stopCamera}
                    >
                      Close Camera
                    </button>
                  </div>
                ) : !previewSrc ? (
                  <div className="empty-box">No input selected</div>
                ) : mode === "video" || selectedFile?.type?.startsWith("video/") ? (
                  <video src={previewSrc || recordedVideoUrl} controls className="w-100 rounded-4" />
                ) : (
                  <div className="preview-wrap">
                    <img src={previewSrc} alt="input" className="plain-preview" />
                  </div>
                )}

                <canvas ref={canvasRef} style={{ display: "none" }} />
              </div>
            </div>
          </div>

          <div className="col-lg-5">
            <div className="card app-card shadow-sm h-100">
              <div className="card-body">
                <h4 className="section-title">Processed Output</h4>

                {!processedSrc ? (
                  <div className="empty-box">No output yet</div>
                ) : mode === "video" ? (
                  <video src={processedSrc} controls className="w-100 rounded-4" />
                ) : (
                  <PreviewWithOverlay src={processedSrc} detections={detections} />
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <ResultsPanel summary={summary} detections={detections} />
        </div>

        <div className="mt-4">
          <Insights stats={stats} />
        </div>
      </main>

      <DetectionsModal
        show={showDetections}
        onClose={() => setShowDetections(false)}
        detections={detections}
      />
    </div>
  );
}

export default App;