import React from 'react';
import { Clock } from "lucide-react";

export default function SegmentNavigator({ segments, activeSegment, onSegmentSelect }) {
  if (!segments || segments.length === 0) return null;
  
  return (
    <div style={{ background: '#111', padding: '20px', borderRadius: '12px', border: '1px solid #333', maxHeight: '500px', overflowY: 'auto' }}>
      <h3 style={{ color: '#888', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '15px' }}>Segments</h3>
      {segments.map((seg, idx) => (
        <button 
          key={idx}
          onClick={() => onSegmentSelect(idx)}
          style={{ 
            width: '100%', textAlign: 'left', padding: '12px', marginBottom: '8px', borderRadius: '8px', border: '1px solid transparent',
            background: activeSegment === idx ? 'rgba(249, 115, 22, 0.15)' : 'transparent',
            color: activeSegment === idx ? '#f97316' : '#ccc',
            borderLeft: activeSegment === idx ? '3px solid #f97316' : '3px solid transparent',
            cursor: 'pointer'
          }}
        >
          <div style={{ fontWeight: 'bold', fontSize: '14px' }}>Segment {seg.topic_id || idx + 1}</div>
          <div style={{ fontSize: '11px', opacity: 0.7, display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Clock size={10} /> {seg.start_time}
          </div>
        </button>
      ))}
    </div>
  );
}