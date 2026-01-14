import { useEffect, useRef } from "react";
import WaveSurfer from "wavesurfer.js";
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions";
import "./Waveform.css";

export default function Waveform({ audioUrl, segments = [] }) {
  const containerRef = useRef(null);
  const waveRef = useRef(null);

  useEffect(() => {
    if (!audioUrl || !containerRef.current) return;

    if (waveRef.current) {
      waveRef.current.destroy();
    }

    waveRef.current = WaveSurfer.create({
      container: containerRef.current,
      waveColor: "#e0e7ff",
      progressColor: "#6366f1",
      cursorColor: "#111827",
      height: 120,
      barWidth: 2,
      responsive: true,
      normalize: true,
      plugins: [RegionsPlugin.create()],
    });

    console.log("WAVEFORM AUDIO 👉", audioUrl);
    waveRef.current.load(audioUrl);

    waveRef.current.on("ready", () => {
      console.log("WAVE READY");

      segments.forEach((seg) => {
        if (!seg.start_time) return;

        const [m, s] = seg.start_time.split(":").map(Number);
        const start = m * 60 + s;
        const end = start + 30; // fallback duration

        waveRef.current.addRegion({
          start,
          end,
          color:
            seg.sentiment === "POSITIVE"
              ? "rgba(34,197,94,0.25)"
              : seg.sentiment === "NEGATIVE"
              ? "rgba(239,68,68,0.25)"
              : "rgba(99,102,241,0.25)",
        });
      });
    });

    return () => waveRef.current?.destroy();
  }, [audioUrl, segments]);

  return (
    <div className="waveform-wrapper">
      <div ref={containerRef} className="waveform-canvas" />
      <button onClick={() => waveRef.current?.playPause()}>
        ▶ Play / Pause
      </button>
    </div>
  );
}
