import "./Features.css";
import img1 from "../assets/img1.jpg";
import img2 from "../assets/img2.jpg";
import img3 from "../assets/img3.jpg";
import img4 from "../assets/img4.jpg";

export default function Features() {
  const items = [
    { title: "Lightning Fast Transcription", image: img1, iconBg: "bg-orange", desc: "Advanced speech recognition converts audio to text in minutes, not hours." },
    { title: "Intelligent Topic Segmentation", image: img2, iconBg: "bg-purple", desc: "NLP algorithms automatically identify topic changes and segment your transcript." },
    { title: "Smart Search & Navigation", image: img3, iconBg: "bg-blue", desc: "Find any topic or phrase instantly. Jump to moments easily." },
    { title: "AI-Generated Summaries", image: img4, iconBg: "bg-green", desc: "Get concise summaries of each topic segment with extracted keywords." },
  ];

  return (
    <section className="features-section">
      <div className="section-header">
        <h2>Powerfull Features

</h2>
        <p className="badge-text">Leveraging state-of-the-art speech recognition and natural language processing
</p>
        
      </div>
      <div className="features-grid">
        {items.map((item, i) => (
          <div key={i} className="feature-card">
            <div className={`feature-img-box ${item.iconBg}`}>
              <img src={item.image} alt={item.title} />
            </div>
            <h3>{item.title}</h3>
            <p>{item.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}