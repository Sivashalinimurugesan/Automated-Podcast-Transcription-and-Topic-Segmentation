import { useEffect, useState } from "react";
import Waveform from "../components/Waveform";
import SentimentGraph from "../components/SentimentGraph";
import "./Analytics.css";

export default function Analytics() {
  const [segments, setSegments] = useState([]);
  const [audioUrl, setAudioUrl] = useState("");

  useEffect(() => {
    const stored = localStorage.getItem("podcastResult");
    if (stored) {
      const parsed = JSON.parse(stored);
      console.log("ANALYTICS DATA 👉", parsed);

      setSegments(parsed.segments || []);
      setAudioUrl(parsed.audioUrl || "");
    }
  }, []);

  if (!segments.length) {
    return <p className="analytics-msg">No analytics data found</p>;
  }

  return (
    <div className="analytics-page">
      <h1>Podcast Analytics</h1>

      {/* 🎧 Waveform */}
      <div className="analytics-card">
        <h3>Waveform Timeline</h3>
        <div className="waveform-box">
          <Waveform audioUrl={audioUrl} segments={segments} />
        </div>
      </div>

      {/* 📊 Sentiment */}
      <div className="analytics-card chart-box">
        <SentimentGraph segments={segments} />
      </div>
    </div>
  );
}
