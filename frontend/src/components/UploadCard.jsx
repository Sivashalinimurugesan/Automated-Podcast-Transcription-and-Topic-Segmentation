import "./UploadCard.css";
import { useState } from "react";
import { uploadAudio } from "../api";
import PodcastResult from "./PodcastResult";

export default function UploadCard() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [activeMode, setActiveMode] = useState("summarize"); // Default mode

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith("audio/")) {
      setFile(selectedFile);
      setResult(null);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleStartProcessing = async () => {
    if (!file) return alert("Please upload an audio file first.");
    setLoading(true);
    try {
      // activeMode decide karega ki backend kya output dega
      const data = await uploadAudio(file, activeMode); 
      setResult(data);
    } catch (err) {
      alert("Processing failed. Check your backend connection.");
    }
    setLoading(false);
  };

  return (
    <div className="main-page-wrapper">
      <div className="center-card">
        <h1 className="main-h1">Podcast Transcriber</h1>
        <p className="main-p">AI-powered speech recognition to transform your podcasts</p>

        <div className="upload-container-inner">
          {/* Mode Selection Buttons */}
          <div className="mode-selector">
            <button 
              className={`mode-btn ${activeMode === "transcribe" ? "active" : ""}`}
              onClick={() => setActiveMode("transcribe")}
            >
              Transcribe Only
            </button>
            <button 
              className={`mode-btn ${activeMode === "summarize" ? "active" : ""}`}
              onClick={() => setActiveMode("summarize")}
            >
              Transcribe & Summarize
            </button>
          </div>

          {/* Drag & Drop Zone */}
          <div 
            className={`drag-box ${isDragging ? "dragging" : ""} ${file ? "file-ready" : ""}`}
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
            <div className="ui-flex">
               <div className="gradient-mic-circle">
                 <div className="css-mic"></div>
               </div>
               <div className="ui-text">
                 <p className="txt-bold">Drag and Drop Audio</p>
                 <p className="txt-light">
                   {file ? file.name : "Drop your podcast file here, or click to browse"}
                 </p>
                 <p className="txt-tiny">Supported: MP3, WAV, M4A (Max 500MB)</p>
               </div>
            </div>
          </div>

          {/* Main Processing Button */}
          <button 
            onClick={handleStartProcessing} 
            disabled={loading || !file} 
            className="big-start-btn"
          >
            {loading ? <span className="spinner"></span> : " Start Processing"}
          </button>
        </div>
      </div>

      {result && <PodcastResult result={result} />}
    </div>
  );
}