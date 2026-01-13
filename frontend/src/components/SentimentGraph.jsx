import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
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
    { sentiment: "POSITIVE", count: counts.POSITIVE || 0 },
    { sentiment: "NEUTRAL", count: counts.NEUTRAL || 0 },
    { sentiment: "NEGATIVE", count: counts.NEGATIVE || 0 }
  ];

  return (
    <div style={{ width: "100%", height: 300, marginTop: 40 }}>
      <h3>Overall Sentiment Analysis</h3>

      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="sentiment" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#6a5cff" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
