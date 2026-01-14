import React, { useState, useRef } from "react";
import "./PodcastResult.css";
import Waveform from "./Waveform";

export default function PodcastResult({ result, mode }) {
  const [searchTerm, setSearchTerm] = useState("");
  const audioRef = useRef(null);

  if (!result) return null;
  const segments = result.segments || [];

  const jumpToSegment = (timeStr, index) => {
    if (audioRef.current && timeStr) {
      const [mins, secs] = timeStr.split(":").map(Number);
      audioRef.current.currentTime = mins * 60 + secs;
      audioRef.current.play();
    }
    const element = document.getElementById(`seg-${index}`);
    if (element) element.scrollIntoView({ behavior: "smooth" });
  };

  const filteredSegments = segments.filter(
    (seg) =>
      seg.text?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      seg.keywords?.some((k) => k.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="podcast-dashboard">

      {/* 🔹 AUDIO + WAVEFORM ONLY ON TOP */}
      <div className="main-audio-box">
        <audio ref={audioRef} controls src={result.audioUrl} />
        {mode === "summarize" && <Waveform audioUrl={result.audioUrl} segments={segments} />}
      </div>

      {/* SEARCH BAR */}
      <input
        type="text"
        placeholder="Search keywords..."
        className="search-input"
        onChange={(e) => setSearchTerm(e.target.value)}
      />

      {/* SEGMENTS */}
      <div className="segments-container">
        {filteredSegments.map((seg, index) => (
          <div key={index} id={`seg-${index}`} className="segment-row-card">

            <div className="col-meta">
              <div className="seg-label">SEGMENT {index + 1}</div>
              <div className="seg-timestamp">{seg.start_time} – {seg.end_time}</div>
              <div className="keywords-container">
                {seg.keywords?.map((word, i) => (
                  <span key={i} className="keyword-highlight">{word}</span>
                ))}
              </div>
            </div>

            <div className="col-text">
              <h5>Transcript</h5>
              <p>{seg.text}</p>
            </div>

            <div className="col-summary">
              <h5>AI Summary</h5>
              <p>{seg.summary}</p>
            </div>

      
          </div>
        ))}
      </div>
    </div>
  );
}
