import React, { useState, useRef } from "react";
import "./PodcastResult.css";
import SentimentGraph from "./SentimentGraph";
export default function PodcastResult({ result, mode }) {
  const [searchTerm, setSearchTerm] = useState("");
  const audioRef = useRef(null);

  if (!result) return null;

  const segments = result.segments || [];

  const jumpToSegment = (timeStr, index) => {
    if (audioRef.current) {
      const [mins, secs] = timeStr.split(":").map(Number);
      audioRef.current.currentTime = mins * 60 + secs;
      audioRef.current.play();
    }
    const element = document.getElementById(`seg-${index}`);
    if (element) element.scrollIntoView({ behavior: "smooth" });
  };

  const filteredSegments = segments.filter(
    (seg) =>
      seg.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
      seg.keywords.some((k) =>
        k.toLowerCase().includes(searchTerm.toLowerCase())
      )
  );

  // TRANSCRIBE ONLY
  if (mode === "transcribe") {
    return (
      <div className="podcast-dashboard">
        <audio ref={audioRef} controls src={result.audioUrl} />
        <div className="simple-transcript">
          <h3>Transcript</h3>
          <p>{result.text}</p>
        </div>
      </div>
    );
  }

  // SUMMARIZE MODE
  return (
    <div className="podcast-dashboard">
      <div className="viz-container">
        <div className="main-audio-box">
          <audio ref={audioRef} controls src={result.audioUrl} />
        </div>

        <h3>Interactive Segment Timeline</h3>
        <div className="timeline-bar">
          {segments.map((seg, i) => (
            <div
              key={i}
              className={`timeline-segment ${seg.sentiment || "NEUTRAL"}`}
              title={`Topic ${i + 1}: ${seg.sentiment}`}
              onClick={() => jumpToSegment(seg.start_time, i)}
            ></div>
          ))}
        </div>
      </div>

      <div className="main-content-split">
        <aside className="navigation-sidebar">
          <h4>Topic Index</h4>
          <input
            type="text"
            placeholder="Search keywords..."
            className="search-input"
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <div className="index-list">
            {filteredSegments.map((seg, i) => (
              <button
                key={i}
                className="index-item"
                onClick={() => jumpToSegment(seg.start_time, i)}
              >
                <span className="idx-time">{seg.start_time}</span>
                <span className="idx-label">Topic {i + 1}</span>
              </button>
            ))}
          </div>
        </aside>

        <div className="display-area">
          {filteredSegments.map((seg, index) => (
            <div key={index} id={`seg-${index}`} className="segment-row-card">
              <div className="col-meta">
                <div className="seg-label">SEGMENT {index + 1}</div>
                <div className="seg-timestamp">
                  {seg.start_time} – {seg.end_time}
                </div>
                <div className="keywords-container">
                  {seg.keywords.map((word, i) => (
                    <span key={i} className="keyword-highlight">
                      {word.toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>

              <div className="col-text">
                <h5>Transcript</h5>
                <p>{seg.text}</p>
              </div>

              <div className="col-summary">
                <h5>AI Summary</h5>
                <div className="summary-box">
                  <p>{seg.summary}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
