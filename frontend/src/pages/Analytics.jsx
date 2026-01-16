import { useState, useEffect } from "react";
import Waveform from "../components/Waveform";
import SentimentGraph from "../components/SentimentGraph";
import TopKeywords from "../components/TopKeywords";
import "./Analytics.css";

export default function Analytics() {
  const [segments, setSegments] = useState([]);
  const [audioUrl, setAudioUrl] = useState("");
  const [viewMode, setViewMode] = useState("sentiment"); // 'sentiment' or 'keywords'

  useEffect(() => {
    const stored = localStorage.getItem("podcastResult");
    if (stored) {
      const parsed = JSON.parse(stored);
      setSegments(parsed.segments || []);
      setAudioUrl(parsed.audioUrl || "");
    }
  }, []);

  if (!audioUrl) return <p className="analytics-msg">No audio found</p>;

  return (
    <div className="analytics-page">
      {/* Top Action Bar with Left Aligned Button */}
      <div className="analytics-action-bar">
        <button 
          className={`top-left-btn ${viewMode === "keywords" ? "active" : ""}`}
          onClick={() => setViewMode(viewMode === "keywords" ? "sentiment" : "keywords")}
        >
          {viewMode === "keywords" ? "Back to Sentiment" : "🔍 Top Keywords"}
        </button>
        <h1>Podcast Analytics</h1>
      </div>

      <div className="analytics-card">
        <h3>Waveform Timeline</h3>
        <div className="waveform-box">
          <Waveform audioUrl={audioUrl} segments={segments} />
        </div>
      </div>

      <div className="analytics-card main-viz-area">
        {viewMode === "keywords" ? (
          <TopKeywords segments={segments} />
        ) : (
          <>
            <h3>Overall Sentiment Analysis</h3>
            <SentimentGraph segments={segments} />
          </>
        )}
      </div>
    </div>
  );
}