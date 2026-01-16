import { useEffect, useRef, useState } from "react";
import WaveSurfer from "wavesurfer.js";
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions.esm.js";

export default function Waveform({ audioUrl, segments = [] }) {
  const containerRef = useRef(null);
  const waveRef = useRef(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!audioUrl || !containerRef.current) return;

    // 1. Initialize Regions Plugin [cite: 31, 32]
    const wsRegions = RegionsPlugin.create();

    // 2. WaveSurfer Instance 
    waveRef.current = WaveSurfer.create({
      container: containerRef.current,
      waveColor: "#e2e8f0",
      progressColor: "#6366f1",
      cursorColor: "#4f46e5",
      height: 100,
      barWidth: 2,
      barGap: 3,
      responsive: true,
      plugins: [wsRegions],
    });

    waveRef.current.load(audioUrl);

    // 3. Logic to Add Topic Segments [cite: 32, 205]
    waveRef.current.on("ready", () => {
      setIsReady(true);
      segments.forEach((seg, index) => {
        if (!seg.start_time) return;
        const [m, s] = seg.start_time.split(":").map(Number);
        const startTime = m * 60 + s;
        
        // Topic Boundary Visualization 
        wsRegions.addRegion({
          start: startTime,
          end: startTime + 2, // Highlight the beginning of a topic
          content: `T${index + 1}`,
          color: "rgba(99, 102, 241, 0.4)",
          drag: false,
          resize: false,
        });
      });
    });

    return () => waveRef.current?.destroy();
  }, [audioUrl, segments]);

  return (
    <div className="waveform-outer-card">
      <div ref={containerRef} className="waveform-main" />
      <div className="waveform-controls">
        <button 
          className="play-btn"
          onClick={() => waveRef.current?.playPause()}
          disabled={!isReady}
        >
          {isReady ? "Play / Pause" : "Loading Waveform..."}
        </button>
      </div>
    </div>
  );
}