// src/App.jsx
import React, { useState, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import './App.css'; // This connects the design!

function App() {
  const [view, setView] = useState('dashboard'); // 'dashboard', 'search', 'sentiment', 'settings'
  const [file, setFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  
  // Settings
  const [autoPlay, setAutoPlay] = useState(true);
  const [highContrast, setHighContrast] = useState(false);

  const audioRef = useRef(null);

  // --- HELPERS ---
  const parseTime = (val) => {
    if (!val) return 0;
    if (typeof val === 'number') return val;
    const parts = val.toString().split(':').map(Number);
    return parts.length === 2 ? parts[0]*60 + parts[1] : 0;
  };

  const getSentimentIcon = (score) => {
    if (score > 0.1) return "😊";
    if (score < -0.1) return "☹️";
    return "😐";
  };

  const highlightText = (text, query) => {
    if (!query) return text;
    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, i) => 
      part.toLowerCase() === query.toLowerCase() ? <span key={i} className="highlight">{part}</span> : part
    );
  };

  // --- HANDLERS ---
  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setAudioUrl(URL.createObjectURL(e.target.files[0]));
      setTopics([]);
      setSelectedTopic(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const fd = new FormData();
    fd.append('file', file);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/upload', { method: 'POST', body: fd });
      const data = await res.json();
      
      if (res.ok) {
        const rawTopics = data.topics || [];
        const processedTopics = rawTopics.map((t, i) => {
            const nextStart = rawTopics[i + 1] ? rawTopics[i + 1].start_time : "End";
            return {
                ...t,
                end_time: nextStart,
                sentimentLabel: t.sentiment > 0.1 ? 'Positive' : t.sentiment < -0.1 ? 'Negative' : 'Neutral'
            };
        });

        setTopics(processedTopics);
        if (processedTopics.length > 0) setSelectedTopic(processedTopics[0]);
        
      } else {
        alert("Server Error: " + data.error);
      }
    } catch (e) { 
        console.error(e);
        alert("Backend Offline"); 
    } finally { 
        setLoading(false); 
    }
  };

  const handleSegmentClick = (topic) => {
    setSelectedTopic(topic);
    if(audioRef.current && autoPlay) {
      audioRef.current.currentTime = parseTime(topic.start_time);
      audioRef.current.play();
    }
  };

  // --- RENDER FUNCTIONS ---

  const renderDashboard = () => (
    <div className="main-grid view-container">
      <div className="left-panel">
        <div className="upload-card">
          <h3 style={{margin:'0 0 10px 0', color:'#fff'}}>{file ? "File Ready" : "Upload Audio"}</h3>
          <div style={{fontSize:'0.8rem', color:'#888', marginBottom:'15px'}}>{file ? file.name : "Drag & Drop MP3 / WAV"}</div>
          <input type="file" id="fIn" hidden onChange={handleFileChange} />
          {!file ? <label htmlFor="fIn" className="upload-btn" style={{color:'#000'}}>Select File</label> 
                 : <button className="upload-btn" onClick={handleUpload} disabled={loading}>{loading ? "Analyzing..." : "Start AI Process"}</button>}
        </div>

        <div className="segment-container">
          <div className="panel-header" style={{marginBottom:'10px', color:'#fff', fontWeight:'bold'}}>Segmentation Results</div>
          <div className="scroll-area">
            {topics.length > 0 ? (
              topics.map((t, i) => (
                <div key={i} className={`segment-row ${selectedTopic === t ? 'active' : ''}`} onClick={() => handleSegmentClick(t)}>
                  <div className="seg-id">Segment {t.topic_id} {getSentimentIcon(t.sentiment)}</div>
                  <div className="seg-time">{t.start_time} ➝ {t.end_time}</div>
                </div>
              ))
            ) : <div className="empty-text">Segments will appear here.</div>}
          </div>
        </div>
      </div>

      <div className="right-panel">
        <div className="audio-box">
           <div style={{marginBottom:'10px', fontSize:'0.9rem', color:'#888'}}>AUDIO PLAYBACK</div>
           {audioUrl ? <audio ref={audioRef} controls src={audioUrl} style={{width:'100%'}} /> : <div style={{textAlign:'center', color:'#555'}}>No Audio Loaded</div>}
        </div>

        <div className="feature-section" style={{flex:1}}>
          <div className="feature-title">
             <span>📝 Executive Summary</span>
             {selectedTopic && (
                <span style={{fontSize:'0.9rem', color:'#888', marginLeft:'auto', display:'flex', alignItems:'center', gap:'8px'}}>
                    Mood: <span style={{color: selectedTopic.sentiment > 0 ? '#22c55e' : '#ff4b4b'}}>{selectedTopic.sentimentLabel}</span> 
                    <span style={{background:'#333', padding:'2px 8px', borderRadius:'4px', fontSize:'0.8rem'}}>
                        {selectedTopic.sentiment.toFixed(2)}
                    </span>
                </span>
             )}
          </div>
          <div className="summary-content" style={{color:'#ddd', lineHeight:'1.6'}}>
            {selectedTopic ? selectedTopic.summary : <div className="empty-text" style={{textAlign:'left'}}>Select a segment.</div>}
          </div>
          <div style={{marginTop:'20px', display:'flex', gap:'8px', flexWrap:'wrap'}}>
             {selectedTopic && selectedTopic.keywords.map(kw => <span key={kw} className="glow-tag">#{kw}</span>)}
          </div>
        </div>
      </div>
    </div>
  );

  const renderSearch = () => {
    const filtered = topics.filter(t => 
      t.summary.toLowerCase().includes(searchQuery.toLowerCase()) || 
      t.keywords.some(k => k.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    return (
      <div className="search-container view-container" style={{maxWidth:'800px', margin:'0 auto'}}>
        <h2 style={{color:'white', marginTop:0}}>Global Search</h2>
        <input type="text" className="search-bar" placeholder="Search keywords..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
        <div className="search-results">
          {filtered.length > 0 ? filtered.map((t, i) => (
            <div key={i} className="result-card" style={{background:'rgba(255,255,255,0.05)', padding:'15px', borderRadius:'8px', marginBottom:'15px', cursor:'pointer'}} onClick={() => { setView('dashboard'); handleSegmentClick(t); }}>
              <div style={{display:'flex', justifyContent:'space-between', marginBottom:'10px'}}>
                <span className="seg-id">Segment {t.topic_id} {getSentimentIcon(t.sentiment)}</span>
                <span className="seg-time">{t.start_time} ➝ {t.end_time}</span>
              </div>
              <p style={{color:'#ccc', margin:0}}>{highlightText(t.summary, searchQuery)}</p>
              <div style={{marginTop:'10px', display:'flex', gap:'5px'}}>
                 {t.keywords.map(k => <span key={k} style={{fontSize:'0.8rem', color:'#00f2ff'}}>#{highlightText(k, searchQuery)}</span>)}
              </div>
            </div>
          )) : <div className="empty-text">{topics.length === 0 ? "No analysis data." : "No matching results."}</div>}
        </div>
      </div>
    );
  };

  const renderSentiment = () => {
    // 2. FIXED TOOLTIP (No 'label' error)
    const CustomTooltip = ({ active, payload }) => {
      if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
          <div style={{ backgroundColor: 'rgba(22, 25, 32, 0.95)', border: '1px solid #00f2ff', padding: '15px', borderRadius:'8px', color: '#fff', minWidth:'150px' }}>
            <h4 style={{ margin: '0 0 5px 0', color:'#00f2ff' }}>Segment {data.topic_id}</h4>
            <div style={{fontSize:'0.85rem', color:'#ccc', marginBottom:'10px'}}>
              Time: {data.start_time} ➝ {data.end_time}
            </div>
            <div style={{ fontWeight:'bold', fontSize:'1rem'}}>
               {getSentimentIcon(data.sentiment)} {data.sentimentLabel}
            </div>
            <div style={{ fontSize:'0.8rem', color:'#888', marginTop:'5px'}}>
               Score: {data.sentiment.toFixed(2)}
            </div>
          </div>
        );
      }
      return null;
    };

    return (
      <div className="settings-container view-container" style={{maxWidth:'1000px', margin:'0 auto'}}>
        <h2 style={{color:'white'}}>Sentiment Timeline</h2>
        <p style={{color:'#888'}}>Interactive timeline showing emotional tone across the podcast.</p>
        
        <div style={{width: '100%', height: 400, marginTop:'30px', background:'rgba(0,0,0,0.2)', padding:'20px', borderRadius:'16px'}}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={topics} onClick={(e) => { if(e && e.activePayload) handleSegmentClick(e.activePayload[0].payload); }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="start_time" stroke="#888" />
              <YAxis domain={[-1, 1]} stroke="#888" />
              <ReferenceLine y={0} stroke="#666" strokeDasharray="3 3" />
              <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#00f2ff', strokeWidth: 1 }} />
              <Line type="monotone" dataKey="sentiment" stroke="#00f2ff" strokeWidth={3} dot={{r: 6}} activeDot={{r: 8, stroke:'#fff'}} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <p style={{textAlign:'center', color:'#555', marginTop:'10px'}}>Click on any data point to jump to that segment.</p>
      </div>
    );
  };

  const renderSettings = () => (
    <div className="settings-container view-container" style={{maxWidth:'800px', margin:'0 auto'}}>
      <h2 style={{color:'white', marginTop:0, borderBottom:'1px solid #333', paddingBottom:'20px'}}>Configuration</h2>
      <div className="setting-row">
        <div className="setting-label"><h4>Auto-Play Segment</h4><p>Automatically play audio when clicking a segment.</p></div>
        <div className={`toggle-switch ${autoPlay ? 'on' : ''}`} onClick={() => setAutoPlay(!autoPlay)}></div>
      </div>
      <div className="setting-row">
        <div className="setting-label"><h4>High Contrast Mode</h4><p>Increase visibility of text and borders.</p></div>
        <div className={`toggle-switch ${highContrast ? 'on' : ''}`} onClick={() => setHighContrast(!highContrast)}></div>
      </div>
      <div className="setting-row" style={{border:0}}>
        <button className="danger-btn" onClick={() => { setTopics([]); setFile(null); setAudioUrl(null); }}>Clear All Data & Reset</button>
      </div>
    </div>
  );

  return (
    <div className="app-container">
      {/* 1. ORIGINAL HEADER: Only the 4 buttons you want */}
      <header className="glass-header">
        <div className="brand">AI PODCAST ANALYZER</div>
        <div className="nav-pills">
          <button className={`pill-btn ${view === 'dashboard' ? 'active' : ''}`} onClick={() => setView('dashboard')}>Dashboard</button>
          <button className={`pill-btn ${view === 'search' ? 'active' : ''}`} onClick={() => setView('search')}>Search</button>
          <button className={`pill-btn ${view === 'sentiment' ? 'active' : ''}`} onClick={() => setView('sentiment')}>Sentiment</button>
          <button className={`pill-btn ${view === 'settings' ? 'active' : ''}`} onClick={() => setView('settings')}>Settings</button>
        </div>
      </header>
      
      {/* VIEW ROUTING */}
      {view === 'dashboard' && renderDashboard()}
      {view === 'search' && renderSearch()}
      {view === 'sentiment' && renderSentiment()}
      {view === 'settings' && renderSettings()}
    </div>
  );
}

export default App;