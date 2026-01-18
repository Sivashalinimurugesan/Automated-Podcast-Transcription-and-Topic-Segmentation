import Plot from "react-plotly.js";
import { useEffect, useState } from "react";

export default function Waveform({ audioUrl }) {
  const [time, setTime] = useState([]);
  const [amplitude, setAmplitude] = useState([]);

  useEffect(() => {
    if (!audioUrl) return;

    // audio filename extract
    const filename = audioUrl.split("/").pop();

    fetch(`http://127.0.0.1:5000/waveform/${filename}`)
      .then((res) => res.json())
      .then((data) => {
        setTime(data.time);
        setAmplitude(data.amplitude);
      })
      .catch((err) => console.error("Waveform error:", err));
  }, [audioUrl]);

  return (
    <Plot
      data={[
        {
          x: time,
          y: amplitude,
          type: "scatter",
          mode: "lines",
        },
      ]}
      layout={{
        title: "Audio Waveform",
        xaxis: { title: "Time (seconds)" },
        yaxis: { title: "Amplitude" },
        height: 250,
        margin: { l: 40, r: 20, t: 40, b: 40 },
      }}
      style={{ width: "100%" }}
      config={{ displayModeBar: false }}
    />
  );
}
