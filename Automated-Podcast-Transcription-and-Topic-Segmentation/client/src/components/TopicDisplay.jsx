import React from 'react';
import { Clock } from "lucide-react";

export default function TopicDisplay({ segment, fileName, activeIndex, totalSegments, onSliderChange }) {
  return (
    <div style={{ background: '#111', padding: '25px', borderRadius: '15px', border: '1px solid #333', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '20px', color: 'white', margin: 0 }}>
          {fileName} — <span style={{ color: '#f97316' }}>Topic {segment.topic_id}</span>
        </h2>
        <div style={{ background: '#222', padding: '5px 15px', borderRadius: '20px', fontSize: '13px', color: '#f97316', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Clock size={14} /> {segment.start_time} - {segment.end_time}
        </div>
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#666', marginBottom: '5px' }}>
        <span>Start</span>
        <span>Segment {activeIndex + 1} of {totalSegments}</span>
        <span>End</span>
      </div>
      <input 
        type="range" min="0" max={totalSegments - 1} value={activeIndex}
        onChange={(e) => onSliderChange(parseInt(e.target.value))}
        style={{ width: '100%', accentColor: '#f97316', cursor: 'pointer' }} 
      />
    </div>
  );
}