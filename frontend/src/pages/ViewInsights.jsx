import PodcastResult from "../components/PodcastResult";
import { useEffect, useState } from "react";
import { uploadAudio } from "../api";
import "./ViewInsights.css";

export default function ViewInsights() {
  const [result, setResult] = useState(null);
  const [mode, setMode] = useState("transcribe");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("podcastResult");
    const storedMode = localStorage.getItem("mode");

    if (stored) setResult(JSON.parse(stored));
    if (storedMode) setMode(storedMode);
  }, []);

  const rerunAnalysis = async (newMode) => {
    const audioURL = sessionStorage.getItem("lastAudioURL");
    if (!audioURL) return alert("Audio not found for rerun");

    setLoading(true);

    try {
      // Fetch audio blob from URL
      const response = await fetch(audioURL);
      const blob = await response.blob();
      const file = new File([blob], "podcastAudio.mp3", { type: blob.type });

      const data = await uploadAudio(file, newMode);

      localStorage.setItem("podcastResult", JSON.stringify(data));
      localStorage.setItem("mode", newMode);

      setMode(newMode);
      setResult(data);
    } catch {
      alert("Backend error during rerun");
    } finally {
      setLoading(false);
    }
  };

  if (!result) return <p>No data found. Please upload an audio first.</p>;

  return (
    <div className="insights-wrapper">
      {/* MODE BUTTONS */}
      <div className="mode-toggle">
        <button
          className={mode === "transcribe" ? "active" : ""}
          onClick={() => rerunAnalysis("transcribe")}
          disabled={loading}
        >
          Transcribe Only
        </button>

        <button
          className={mode === "summarize" ? "active" : ""}
          onClick={() => rerunAnalysis("summarize")}
          disabled={loading}
        >
          Transcribe & Summarize
        </button>
      </div>

      {loading && <p>Re-processing audio...</p>}

      <PodcastResult result={result} mode={mode} />
    </div>
  );
}
