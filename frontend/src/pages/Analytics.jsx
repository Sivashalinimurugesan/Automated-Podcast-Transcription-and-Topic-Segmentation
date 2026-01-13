import { useEffect, useState } from "react";
import SentimentGraph from "../components/SentimentGraph";
import "./Analytics.css";

export default function Analytics() {
  const [segments, setSegments] = useState([]);

  useEffect(() => {
    const stored = localStorage.getItem("podcastResult");
    if (stored) {
      const parsed = JSON.parse(stored);
      setSegments(parsed.segments || []);
    }
  }, []);

  if (segments.length === 0) {
    return <p className="analytics-msg">No analytics data found</p>;
  }

  return (
    <div className="analytics-page">
      <h1>Podcast Analytics</h1>
      <SentimentGraph segments={segments} />
    </div>
  );
}
