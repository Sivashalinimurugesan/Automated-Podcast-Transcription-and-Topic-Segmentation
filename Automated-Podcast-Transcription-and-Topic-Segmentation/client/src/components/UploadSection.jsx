import React from 'react';
import { Upload, Loader2 } from "lucide-react";

export default function UploadSection({ onFileSelect, onUpload, loading, hasFile }) {
  return (
    <div style={{ background: '#111', padding: '20px', borderRadius: '12px', border: '1px solid #333', marginBottom: '20px' }}>
      <h3 style={{ color: '#888', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '15px' }}>Upload Audio</h3>
      <input 
        type="file" 
        onChange={(e) => onFileSelect(e.target.files[0])} 
        style={{ color: '#ccc', fontSize: '14px', marginBottom: '15px', width: '100%' }}
      />
      <button 
        onClick={onUpload} 
        disabled={loading || !hasFile}
        style={{ 
          width: '100%', padding: '12px', borderRadius: '8px', border: 'none', 
          background: loading ? '#555' : '#f97316', color: 'white', fontWeight: 'bold', cursor: 'pointer',
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px'
        }}
      >
        {loading ? <Loader2 className="animate-spin" size={18} /> : <Upload size={18} />}
        {loading ? "Processing..." : "Analyze Audio"}
      </button>
    </div>
  );
}