import React, { useState, useRef } from "react";
import "./PodcastResult.css";
import SentimentGraph from "./SentimentGraph";


export default function PodcastResult({ result, mode }) {
  const [currentTime, setCurrentTime] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const audioRef = useRef(null);

  if (!result) return null;

  const segments = result.segments || [];

  //  "00:23" → seconds
  const timeToSeconds = (time) => {
    if (!time) return 0;
    const [m, s] = time.split(":").map(Number);
    return m * 60 + s;
  };

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
      seg.keywords?.some((k) =>
        k.toLowerCase().includes(searchTerm.toLowerCase())
      )
  );

  //  TRANSCRIBE ONLY MODE
  if (mode === "transcribe") {
    return (
      <div className="podcast-dashboard">
        <audio ref={audioRef} controls src={result.audioUrl} />
        <div className="simple-transcript">
          <h3>Transcript</h3>
          <p>{segments[0]?.text}</p>
        </div>
      </div>
    );
  }

  //  TRANSCRIBE + SUMMARIZE MODE
  return (
    <div className="podcast-dashboard">
      {/*  AUDIO */}
      <div className="viz-container">
        <div className="main-audio-box">
          <audio
            ref={audioRef}
            controls
            src={result.audioUrl}
            onTimeUpdate={() =>
              setCurrentTime(audioRef.current.currentTime)
            }
          />
        </div>

        <h3>Interactive Segment Timeline</h3>
        <div className="timeline-bar">
          {segments.map((seg, i) => (
            <div
              key={i}
              className={`timeline-segment ${seg.sentiment || "NEUTRAL"}`}
              title={`Topic ${i + 1}: ${seg.sentiment || "NEUTRAL"}`}
              onClick={() => jumpToSegment(seg.start_time, i)}
              style={{ flex: 1 }}
            />
          ))}
        </div>
      </div>

      <div className="main-content-split">
        {/*  SIDEBAR */}
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

        {/* SEGMENTS WITH AUTO HIGHLIGHT */}
        <div className="display-area">
          {filteredSegments.map((seg, index) => {
            const start = timeToSeconds(seg.start_time);
            const end = timeToSeconds(seg.end_time);

            const isActive =
              currentTime >= start && currentTime <= end;

            return (
              <div
                key={index}
                id={`seg-${index}`}
                className={`segment-row-card ${
                  isActive ? "active" : ""
                }`}
              >
                <div className="col-meta">
                  <div className="seg-label">
                    SEGMENT {index + 1}
                  </div>
                  <div className="seg-timestamp">
                    {seg.start_time} – {seg.end_time}
                  </div>

                  <div className="keywords-container">
                    {seg.keywords?.map((word, i) => (
                      <span
                        key={i}
                        className="keyword-highlight"
                      >
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
            );
          })}
        </div>
      </div>
    </div>
  );
}
