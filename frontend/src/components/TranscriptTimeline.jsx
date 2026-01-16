import { useEffect, useRef } from "react";
import "./TranscriptTimeline.css";

export default function TranscriptTimeline({ segments, currentTime }) {
  const activeRef = useRef(null);

  useEffect(() => {
    if (activeRef.current) {
      activeRef.current.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  }, [currentTime]);

  return (
    <div className="transcript-wrapper">
      <h3>Transcript</h3>

      {segments.map((seg, i) => {
        const active = currentTime >= seg.start && currentTime <= seg.end;

        return (
          <p
            key={i}
            ref={active ? activeRef : null}
            className={`transcript-line ${active ? "active" : ""}`}
          >
            <b>[{seg.start.toFixed(1)}s]</b> {seg.text}
          </p>
        );
      })}
    </div>
  );
}
