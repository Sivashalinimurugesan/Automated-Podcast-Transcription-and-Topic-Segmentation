import React from "react";

const SegmentSentiment = ({ segments }) => {
  const counts = { POSITIVE: 0, NEGATIVE: 0, NEUTRAL: 0 };

  segments.forEach(s => {
    if (s.sentiment?.label) {
      counts[s.sentiment.label] =
        (counts[s.sentiment.label] || 0) + 1;
    }
  });

  return (
    <div>
      <h3>Segment Sentiment Distribution</h3>

      <ul>
        <li>Positive: {counts.POSITIVE}</li>
        <li>Negative: {counts.NEGATIVE}</li>
        <li>Neutral: {counts.NEUTRAL}</li>
      </ul>

      <div className="segment-list">
        {segments.map(seg => (
          <div key={seg.segment_id} className="segment-card">
            <p><b>Segment {seg.segment_id}</b></p>
            <p>{seg.segment_summary}</p>
            <p>
              Sentiment:
              <span style={{ marginLeft: "8px" }}>
                {seg.sentiment?.label} ({seg.sentiment?.score})
              </span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SegmentSentiment;
