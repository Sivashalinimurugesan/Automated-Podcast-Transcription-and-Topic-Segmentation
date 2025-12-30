import "./PodcastResult.css";

export default function PodcastResult({ result, audioUrl }) {
  if (!result) return null;

  const segments = result.segments || [];

  return (
    <div className="podcast-result">

      {/* 🎧 Audio Player */}
      {audioUrl && (
        <div className="audio-player">
          <audio controls src={audioUrl} />
        </div>
      )}

      {/* 📌 Segments */}
      <h2 className="title">Podcast Segments</h2>

      {segments.length === 0 && (
        <p className="empty">No segments found</p>
      )}

      {segments.map((seg, index) => (
        <div key={index} className="segment-card">

          {/* Time */}
          <div className="time">
            ⏱ {seg.start_time} – {seg.end_time}
          </div>

          <div className="content">

            {/* Transcript */}
            <div className="text">
              <p>{seg.text}</p>

              {/* Keywords */}
              <div className="keywords">
                {seg.keywords.map((word, i) => (
                  <span key={i} className="keyword">
                    {word}
                  </span>
                ))}
              </div>
            </div>

            {/* Summary */}
            <div className="summary">
              <h4>Summary</h4>
              <p>{seg.summary}</p>
            </div>

          </div>
        </div>
      ))}
    </div>
  );
}
