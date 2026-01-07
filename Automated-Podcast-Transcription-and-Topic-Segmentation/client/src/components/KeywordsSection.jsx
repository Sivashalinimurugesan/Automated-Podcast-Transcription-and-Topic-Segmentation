import React from 'react';
import { Hash } from "lucide-react";

export default function KeywordsSection({ keywords }) {
  return (
    <div style={{ marginBottom: '25px' }}>
      <h3 style={{ color: '#888', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Hash size={14} /> Keywords Extraction
      </h3>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        {keywords && keywords.map((k, i) => (
          <span key={i} style={{ background: 'rgba(14, 165, 233, 0.1)', color: '#0ea5e9', border: '1px solid rgba(14, 165, 233, 0.3)', padding: '5px 15px', borderRadius: '20px', fontSize: '13px' }}>
            #{k}
          </span>
        ))}
      </div>
    </div>
  );
}