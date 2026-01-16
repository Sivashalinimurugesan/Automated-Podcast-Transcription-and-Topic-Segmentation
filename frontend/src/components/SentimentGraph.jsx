import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell // 👈 Ye import zaroor add karein
} from "recharts";

export default function SentimentGraph({ segments }) {

  if (!segments || segments.length === 0) {
    return <p>No sentiment data available</p>;
  }

  const counts = segments.reduce((acc, seg) => {
    const s = seg.sentiment || "NEUTRAL";
    acc[s] = (acc[s] || 0) + 1;
    return acc;
  }, {});

  const data = [
    { sentiment: "POSITIVE", count: counts.POSITIVE || 0, color: "#22c55e" }, // Green
    { sentiment: "NEUTRAL", count: counts.NEUTRAL || 0, color: "#6366f1" },   // Blue/Indigo
    { sentiment: "NEGATIVE", count: counts.NEGATIVE || 0, color: "#ef4444" }  // Red
  ];

  return (
    <div style={{ width: "100%", height: 300, marginTop: 40 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="sentiment" />
          <YAxis allowDecimals={false} />
          <Tooltip cursor={{fill: 'transparent'}} />
          <Bar dataKey="count">
            {/* 🎨 Mapping through data to apply custom colors to each bar */}
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}