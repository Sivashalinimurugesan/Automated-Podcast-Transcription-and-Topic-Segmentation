import React from 'react';
import { Search, Mic } from "lucide-react";

export default function Header({ searchTerm, onSearchChange }) {
  return (
    <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px', borderBottom: '1px solid #333', paddingBottom: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
        <div style={{ background: '#f97316', padding: '10px', borderRadius: '10px', display: 'flex' }}>
          <Mic size={24} color="white" />
        </div>
        <h1 style={{ fontSize: '26px', fontWeight: 'bold', color: 'white', margin: 0 }}>
          Podcast<span style={{ color: '#f97316' }}>AI</span>
        </h1>
      </div>
      <div style={{ position: 'relative' }}>
        <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#888' }} />
        <input
          type="text"
          placeholder="Global Search..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          style={{ background: '#111', border: '1px solid #333', color: 'white', padding: '10px 10px 10px 40px', borderRadius: '8px', width: '300px' }}
        />
      </div>
    </header>
  );
}