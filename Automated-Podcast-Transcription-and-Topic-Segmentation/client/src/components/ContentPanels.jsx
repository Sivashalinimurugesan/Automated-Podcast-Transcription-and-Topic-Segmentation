import React from 'react';
import { FileText, Sparkles } from "lucide-react";

export default function ContentPanels({ transcript, summary }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <div style={{ background: '#111', padding: '20px', borderRadius: '15px', border: '1px solid #333', height: '400px', display: 'flex', flexDirection: 'column' }}>
        <h4 style={{ color: '#f97316', borderBottom: '1px solid #333', paddingBottom: '10px', marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <FileText size={18} /> Transcript
        </h4>
        <p style={{ color: '#ddd', lineHeight: '1.6', fontSize: '14px', overflowY: 'auto', flex: 1 }}>{transcript}</p>
      </div>
      
      <div style={{ background: '#111', padding: '20px', borderRadius: '15px', border: '1px solid #333', height: '400px', display: 'flex', flexDirection: 'column' }}>
        <h4 style={{ color: '#0ea5e9', borderBottom: '1px solid #333', paddingBottom: '10px', marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles size={18} /> AI Summary
        </h4>
        <div style={{ background: 'rgba(14, 165, 233, 0.05)', borderLeft: '3px solid #0ea5e9', padding: '15px', color: '#eee', lineHeight: '1.6', fontSize: '14px', overflowY: 'auto', flex: 1 }}>
          {summary}
        </div>
      </div>
    </div>
  );
}