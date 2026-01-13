import "./UploadCard.css";
import { useState } from "react";
import { uploadAudio } from "../api";
import { useNavigate } from "react-router-dom";

export default function UploadCard() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const navigate = useNavigate();

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith("audio/")) {
      setFile(selectedFile);
    } else {
      alert("Upload MP3 / WAV / M4A only");
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleStartProcessing = async () => {
    if (!file) return alert("Upload audio first");

    // Clear old data
    localStorage.removeItem("podcastResult");
    localStorage.removeItem("mode");
    sessionStorage.removeItem("lastAudioURL");

    setLoading(true);
    try {
      // DEFAULT: Transcribe Only
      const data = await uploadAudio(file, "transcribe");

      localStorage.setItem("podcastResult", JSON.stringify(data));
      localStorage.setItem("mode", "transcribe");

      // Save audio blob URL for rerun
      const audioBlob = URL.createObjectURL(file);
      sessionStorage.setItem("lastAudioURL", audioBlob);

      navigate("/insights");
    } catch {
      alert("Backend error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-page-wrapper">
      <div className="center-card">
        <h1 className="main-h1">Podcast Transcriber</h1>

        <div
          className={`drag-box ${isDragging ? "dragging" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={onDrop}
        >
          <input
            type="file"
            className="file-ghost-input"
            onChange={(e) => handleFile(e.target.files[0])}
            accept="audio/*"
          />
          <p>{file ? file.name : "Drag & Drop Audio"}</p>
        </div>

        <button
          className="big-start-btn"
          onClick={handleStartProcessing}
          disabled={loading || !file}
        >
          {loading ? "Processing..." : "Start Processing"}
        </button>
      </div>
    </div>
  );
}
