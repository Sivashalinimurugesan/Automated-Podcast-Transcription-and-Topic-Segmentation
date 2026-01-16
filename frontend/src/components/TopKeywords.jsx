import React from 'react';
import ReactWordcloud from 'react-wordcloud';
import './TopKeywords.css';

export default function TopKeywords({ segments }) {
  // 1. Keywords aggregate karne ka logic
  const calculateWordFrequency = () => {
    const counts = {};
    segments.forEach(seg => {
      seg.keywords?.forEach(word => {
        const key = word.toLowerCase();
        counts[key] = (counts[key] || 0) + 1;
      });
    });

    return Object.entries(counts).map(([text, value]) => ({
      text: text.toUpperCase(),
      value: value , 
    }));
  };

  const words = calculateWordFrequency();

  // 2. Word Cloud ke professional settings
  const options = {
    colors: ["#6366f1", "#8b5cf6", "#d946ef", "#f59e0b", "#10b981"],
    fontFamily: "Inter, sans-serif",
    fontSizes: [25, 80], // Mentor ki photo jaisa bada font
    rotations: 1, // Sirf horizontal rakhein professional look ke liye
    rotationAngles: [0, 0],
    scale: "linear",
    spiral: "archimedean",
    transitionDuration: 800,
  };

  if (!segments || segments.length === 0) {
    return <div className="no-data">No analysis data available.</div>;
  }

  return (
    <div className="top-keywords-view">
      <div className="keywords-header">
        <h3>Keyword Explorer (Word Cloud)</h3>
        <p>This visualization identifies the core themes of your podcast.</p>
      </div>
      
      <div className="word-cloud-container">
        {/* Is div ko height dena zaroori hai varna cloud dikhega nahi */}
        <ReactWordcloud words={words} options={options} />
      </div>
    </div>
  );
}