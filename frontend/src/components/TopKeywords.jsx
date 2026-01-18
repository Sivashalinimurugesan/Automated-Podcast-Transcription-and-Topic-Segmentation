import React from 'react';
import ReactWordcloud from 'react-wordcloud';
import './TopKeywords.css';

export default function TopKeywords({ segments }) {
  
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

  
  const options = {
    colors: ["#6366f1", "#8b5cf6", "#d946ef", "#f59e0b", "#10b981"],
    fontFamily: "Inter, sans-serif",
    fontSizes: [25, 80], 
    rotations: 1, 
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
        <h3>Keyword Explorer</h3>
        
      </div>
      
      <div className="word-cloud-container">
        
        <ReactWordcloud words={words} options={options} />
      </div>
    </div>
  );
}