import "./HowItWork.css";
import audio from "../assets/audio.jpg";
import ai from "../assets/ai.jpg";
import topic from "../assets/topic.jpg";
import navi from "../assets/navi.jpg";

export default function HowItWorks() {
  const steps = [
    { title: "Upload Audio", description: "Upload podcast in MP3, WAV, or M4A format.", image: audio },
    { title: "AI Transcription", description: "Our AI transcribes with high accuracy.", image: ai },
    { title: "Topic Segmentation", description: "Identify topic changes automatically.", image: topic },
    { title: "Navigate & Export", description: "Browse and export in your format.", image: navi },
  ];

  const technologies = [
    { label: "Speech-to-Text", name: "Whisper AI" },
    { label: "NLP Engine", name: "GPT-4" },
    { label: "Segmentation", name: "Custom ML" },
    { label: "Indexing", name: "Vector DB" },
  ];

  return (
    <section className="how-section">
      <div className="section-header">
        <h2 className="title-bold-main">How It Works</h2>
        <p className="subtitle-light-main">From audio upload to intelligent segmentation in four simple steps</p>
      </div>

      <div className="how-grid-container">
        {/* Connecting Line from Screenshot */}
        <div className="connecting-line"></div>
        
        <div className="how-grid">
          {steps.map((step, i) => (
            <div key={i} className="how-card">
              <div className="image-container">
                <span className="how-badge">{String(i + 1).padStart(2, "0")}</span>
                <img src={step.image} alt={step.title} />
                {/* Blue dot on the line */}
                <div className="step-dot"></div>
              </div>
              <div className="how-body">
                <h3 className="step-title-bold">{step.title}</h3>
                <p className="step-desc-light">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="tech-bar-modern">
        {technologies.map((t, idx) => (
          <div key={idx} className="tech-unit">
            <span className="unit-label">{t.label}</span>
            <span className="unit-name">{t.name}</span>
          </div>
        ))}
      </div>
    </section>
  );
}