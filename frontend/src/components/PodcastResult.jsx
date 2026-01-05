import React, { useState } from "react";
import "./PodcastResult.css";

export default function PodcastResult({ result, audioUrl, mode }) {
  const [searchTerm, setSearchTerm] = useState("");
  if (!result) return null;

  const segments = result.segments || [];

  // Search logic for navigation [cite: 37]
  const filteredSegments = segments.filter(seg => 
    seg.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
    seg.keywords.some(k => k.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="podcast-dashboard">
      {/* Milestone 5: Visualization Header [cite: 38, 39] */}
      <div className="viz-container">
        <h3>Interactive Segment Timeline</h3>
        <div className="timeline-bar">
          {segments.map((seg, i) => (
            <div 
              key={i} 
              className={`timeline-segment ${seg.sentiment || 'NEUTRAL'}`} 
              title={`Segment ${seg.segment_number}: ${seg.start_time}`}
              style={{ flex: 1 }}
            ></div>
          ))}
        </div>
        <div className="stats-row">
           <div className="stat">Total Topics: {segments.length}</div>
           <div className="stat">Mode: {mode === 'transcribe' ? 'Text Only' : 'AI Analysis'}</div>
        </div>
      </div>

      <div className="main-content-split">
        {/*  Milestone 4: Indexing & Navigation Sidebar  */}
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
              <button key={i} className="index-item" onClick={() => document.getElementById(`seg-${i}`).scrollIntoView({behavior: 'smooth'})}>
                <span className="idx-time">{seg.start_time}</span>
                <span className="idx-label">Topic {i + 1}</span>
              </button>
            ))}
          </div>
        </aside>

        {/*  Main Transcript & Summary View */}
        <div className="display-area">
          {filteredSegments.map((seg, index) => (
            <div key={index} id={`seg-${index}`} className="segment-row-card">
              {/* Left Column: Metadata  */}
              <div className="col-meta">
                <div className="seg-label">SEGMENT {index + 1}</div>
                <div className="seg-timestamp"> {seg.start_time} – {seg.end_time}</div>
                <div className="keywords-container">
                  {seg.keywords.map((word, i) => (
                    <span key={i} className="keyword-highlight">{word.toUpperCase()}</span>
                  ))}
                </div>
              </div>

              {/* Middle Column: Full Text  */}
              <div className="col-text">
                <h5>Transcript</h5>
                <p>{seg.text}</p>
              </div>

              {/* Right Column: AI Summary [cite: 34] */}
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