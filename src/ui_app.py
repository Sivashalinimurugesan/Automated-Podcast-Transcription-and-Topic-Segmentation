import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import time
from datetime import timedelta
from datetime import datetime
import io
import re

# Import Pipeline Agents
from preprocessing import process_audio
from transcription import Transcriber
from segmentation import TopicSegmenter
from summarization import Summarizer
from keyword_extraction import KeywordExtractor
from indexing import TopicIndexer

from logger import SessionLogger
from sentiment_analysis import SentimentAnalysisAgent
from chatbot import PodcastChatBot

from pydub import AudioSegment

# --- Page Configuration ---
st.set_page_config(
    page_title="Podcast Intelligence",
    layout="wide",
    page_icon="🎙️",
    initial_sidebar_state="expanded" 
)

# --- Constants & Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_RAW_DIR = os.path.join(BASE_DIR, 'audio_raw')
AUDIO_PROCESSED_DIR = os.path.join(BASE_DIR, 'audio_processed')
TRANSCRIPT_DIR = os.path.join(BASE_DIR, 'transcripts')
SEGMENTS_DIR = os.path.join(BASE_DIR, 'segments')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

for d in [AUDIO_RAW_DIR, AUDIO_PROCESSED_DIR, TRANSCRIPT_DIR, SEGMENTS_DIR, LOGS_DIR]:
    os.makedirs(d, exist_ok=True)

# --- Styling ---
CUSTOM_CSS = """
<style>
    /* VARIABLES (Neon Violet Premium Theme) */
    :root {
        --primary: #6c63ff;
        --secondary: #311b92;
        --accent: #FF2E63;
        --bg-color: #F8F9FE;
        --card-bg: rgba(255, 255, 255, 0.9);
        --text-primary: #1A1A40;
        --text-secondary: #5A5A7B;
        --success: #00E676;
        --border-color: rgba(108, 99, 255, 0.2);
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    /* ANIMATIONS */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(108, 99, 255, 0.4); }
        70% { box-shadow: 0 0 0 12px rgba(108, 99, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(108, 99, 255, 0); }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* COMPONENT: GLASS CARD */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px -10px rgba(108, 99, 255, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.6s ease-out;
        margin-bottom: 20px;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px -10px rgba(108, 99, 255, 0.25);
        border-color: var(--primary);
    }

    /* COMPONENT: ACTION BUTTONS (Streamlit overrides) */
    div.stButton > button {
        background: white;
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 50px; /* Pill shape */
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    div.stButton > button:hover {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white !important;
        border-color: transparent;
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(108, 99, 255, 0.3);
    }
    
    /* Primary / Active Button styling overrides */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white !important;
        border: none;
        box-shadow: 0 8px 20px rgba(108, 99, 255, 0.3);
    }
    
    /* UPLOAD AREA SPECIFIC */
    .upload-area {
        position: relative;
        background: linear-gradient(to bottom, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
        border: 2px dashed var(--primary);
        border-radius: 24px;
        padding: 50px 20px;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 30px;
        animation: fadeIn 0.8s ease-out;
    }
    .upload-area:hover {
        background: rgba(255, 255, 255, 0.95);
        transform: scale(1.01);
        box-shadow: 0 0 25px rgba(108, 99, 255, 0.15);
        animation: pulse-glow 1.5s infinite;
    }
    
    .icon-box {
        font-size: 4rem;
        margin-bottom: 15px;
        filter: drop-shadow(0 4px 6px rgba(108, 99, 255, 0.2));
    }

    /* TAGS */
    .tag {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(108, 99, 255, 0.1);
        color: var(--primary);
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(108, 99, 255, 0.3);
    }
    
    /* TIMELINE & CHARTS */
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 12px;
        background: rgba(108, 99, 255, 0.05);
        border: 1px solid rgba(108, 99, 255, 0.1);
    }
    
    /* HIDE DEFAULT ELEMENTS */
    /* [data-testid="stSidebar"] { display: none; } */
    footer { visibility: hidden; }

    
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'stop_requested' not in st.session_state:
    st.session_state.stop_requested = False
if 'last_processed_file' not in st.session_state:
    st.session_state.last_processed_file = None
if 'pipeline_step' not in st.session_state:
    st.session_state.pipeline_step = 0
if 'pipeline_file' not in st.session_state:
    st.session_state.pipeline_file = None

if 'last_search' not in st.session_state:
    st.session_state.last_search = None
if 'hf_token' not in st.session_state:
    st.session_state.hf_token = ""

# --- AGENT LOADING ---
@st.cache_resource
def load_agents_v9():
    # Placeholder for loading animation
    with st.spinner("🧠 Initializing Neural Engines (v9)..."):
        transcriber = Transcriber(model_size="base", compute_type="int8")
        segmenter = TopicSegmenter()
        summarizer = Summarizer()
        kw_extractor = KeywordExtractor(method='yake')
        indexer = TopicIndexer()
        sentiment_agent = SentimentAnalysisAgent()
        chatbot = PodcastChatBot()
        
        return transcriber, segmenter, summarizer, kw_extractor, indexer, sentiment_agent, chatbot

transcriber, segmenter, summarizer, kw_extractor, indexer, sentiment_agent, chatbot = load_agents_v9()

@st.cache_resource
def load_audio_file(file_path):
    return AudioSegment.from_file(file_path)

# --- NAVIGATION ---
def render_navbar():
    # Remove default styling and inject standard nav style
    menu_items = {
        "Home": "🏠",
        "Upload": "☁️",
        "Timeline": "⏳",
        "Transcription": "📝"
    }

    # Internal page background reset (Clean Slate)
    st.markdown("""
        <style>
            .stApp {
                background: var(--bg-color);
                background-image: radial-gradient(circle at 10% 20%, rgba(108, 99, 255, 0.05) 0%, transparent 20%),
                                  radial-gradient(circle at 90% 80%, rgba(49, 27, 146, 0.05) 0%, transparent 20%);
                animation: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Nav Container
    st.markdown('<div class="nav-container" style="display:flex; justify-content:center; gap:15px; padding:20px; animation: slideDown 0.5s ease;">', unsafe_allow_html=True)
    
    cols = st.columns(len(menu_items))
    for idx, (label, icon) in enumerate(menu_items.items()):
        with cols[idx]:
            is_active = st.session_state.page == label
            if st.button(f"{icon} {label}", key=f"nav_{label}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.page = label
                st.rerun()
                

                
    st.markdown('</div><div style="height:1px; background:linear-gradient(90deg, transparent, var(--border-color), transparent); margin-bottom:30px;"></div>', unsafe_allow_html=True)
    
    # Sidebar for Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        hf_token = st.text_input(
            "Hugging Face Token", 
            type="password", 
            value=st.session_state.hf_token,
            help="Required for Speaker Diarization (pyannote.audio). Models: pyannote/speaker-diarization-3.1"
        )
        if hf_token != st.session_state.hf_token:
            st.session_state.hf_token = hf_token
            st.rerun()
        
        if st.session_state.hf_token:
            st.success("Token Loaded")
        else:
            st.warning("Diarization Disabled (No Token)")

# --- VIEWS ---

def render_home():
    # Animated Gradient Background specifically for Home
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(-45deg, #EEF2FF, #E0E7FF, #FCE7F3, #F3E8FF);
                background-size: 400% 400%;
                animation: gradient-shift 15s ease infinite;
            }
        </style>
    """, unsafe_allow_html=True)

    hero_html = (
        "<div style='text-align: center; margin-top: 60px; margin-bottom: 60px; animation: fadeIn 1s ease;'>"
        "<h1 style='font-size: 3.5rem; background: linear-gradient(90deg, #6c63ff, #311b92); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>"
        "Podcast Intelligence Engine"
        "</h1>"
        "<p style='font-size: 1.2rem; color: #5A5A7B; margin-top: 10px;'>"
        "AI-powered insights from your conversations & podcasts"
        "</p>"
        "</div>"
    )
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Showcase Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="glass-card" style="text-align:center;">'
            '<div style="font-size: 2rem;">🔍</div>'
            '<h4 style="margin:10px 0;">Automated Transcripts</h4>'
            '<p style="font-size:0.9rem; color:#666;">High-accuracy Whisper ASR with speaker diarization.</p>'
            '</div>', 
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            '<div class="glass-card" style="text-align:center;">'
            '<div style="font-size: 2rem;">🧠</div>'
            '<h4 style="margin:10px 0;">Topic Intelligence</h4>'
            '<p style="font-size:0.9rem; color:#666;">Semantic segmentation and topic discovery.</p>'
            '</div>', 
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            '<div class="glass-card" style="text-align:center;">'
            '<div style="font-size: 2rem;">🎯</div>'
            '<h4 style="margin:10px 0;">Highlights</h4>'
            '<p style="font-size:0.9rem; color:#666;">Key takeaways and summaries extracted automatically.</p>'
            '</div>', 
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("Start Upload →", type="primary", use_container_width=True):
            st.session_state.page = "Upload"
            st.rerun()

def render_upload():
    # --- CSS Overlay for Drag & Drop ---
    # This pulls the st.file_uploader UP over the custom HTML card
    overlay_css = """
    <style>
        .upload-stack {
            position: relative;
            height: 350px; /* match card height */
            margin-bottom: 20px;
        }
        
        /* The Visual Card (Background) */
        .visual-card {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none; /* Let clicks pass through if needed, but we want uploader on top */
        }
        
        /* The Actual Uploader (Foreground, Invisible but Active) */
        div[data-testid="stFileUploader"] {
            position: relative;
            z-index: 5;
            opacity: 0; /* Make invisible */
            height: 350px;
            padding-top: 50px; /* Alignment adjustment */
        }
        
        div[data-testid="stFileUploader"] > section {
            height: 350px;
            cursor: pointer;
        }
        
        /* Hover effect linkage: When hovering uploader, style the card underneath? 
           Hard to do with CSS siblings in this order. 
           Instead, we style the uploader to be "visible" but transparent?
           No, we rely on the visual card's internal animations.
           But to trigger hover on the card when hovering the invisible uploader is tricky.
           We'll set the Uploader to have the 'pointer' cursor.
        */
        
        /* Hide the 'Limit 200MB' text which might bleed through if opacity is weird */
        div[data-testid="stFileUploader"] small {
            display: none;
        }
    </style>
    """
    st.markdown(overlay_css, unsafe_allow_html=True)
    
    # --- UI RENDER ---
    
    # 1. Visual Layer (HTML)
    card_html = (
       '<div class="upload-stack">'
       '<div class="visual-card">'
       '<div class="glass-card" style="height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; animation: fadeIn 0.8s ease;">'
       '<h2 style="color:var(--text-primary); margin:0 0 10px 0;">🚀 Initiate Intelligence Pipeline</h2>'
       '<p style="color:var(--text-secondary); margin:0 0 30px 0;">Upload your podcast audio to extract transcripts, topics, and actionable insights.</p>'
       '<div class="upload-area" style="width:80%;">'
       '<div class="icon-box">🎙️</div>'
       '<h3 style="margin:10px 0; color:var(--text-primary);">Drag & Drop Audio Files</h3>'
       '<p style="color:var(--text-secondary);">Supported: <span style="font-weight:700; color:var(--primary);">MP3, WAV, M4A</span></p>'
       '</div>'
       '</div>'
       '</div>'
       '</div>'
    )
    # We render the Style + Card structure first.
    # Note: Streamlit renders elements sequentially. 
    # To overlap, we need to create a container where we can use negative margins OR 
    # simply place the uploader visually "on top".
    #
    # Actually, the CSS `margin-top: -350px` on the Uploader is the classic trick.
    # Let's render the Card, then the Uploader, then pull Uploader up.
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # 2. Logic Layer (Invisible Uploader)
    # We inject specific style to pull THIS uploader up
    st.markdown(
        """
        <style>
            div[data-testid="stFileUploader"] {
                margin-top: -365px; /* Pull up to overlap the card above */
                height: 350px; /* Match Height */
            }
            div[data-testid="stFileUploader"] section {
                height: 100%;
                background: transparent !important;
                border: none !important;
            }
            div[data-testid="stFileUploader"] button {
               display: none; /* Hide 'Browse files' button if we want pure drag/click area */
            }
            /* We arguably DO want the Browse button available if drag fails, 
               but typically clicking the dropzone opens dialog anyway. */
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Stop Button Logic (Only visible when processing)
    if st.session_state.get('is_processing', False):
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
             if st.button("🛑 Stop Processing", type="primary", use_container_width=True):
                 st.session_state.stop_requested = True
                 st.rerun()
    
    uploaded_file = st.file_uploader("", type=["mp3", "wav", "m4a"], label_visibility="collapsed")
    
    # Spacer to push subsequent content down (since uploader was pulled up, it leaves no gap)
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

    # --- SELECTION & PROCESSING LOGIC ---
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
         st.markdown(
            '<div style="text-align: center; margin-bottom: 15px;">'
            '<span style="background: rgba(108, 99, 255, 0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8em; color: var(--primary); border: 1px solid var(--border-color); font-weight:600;">'
            'OR SELECT EXISTING FROM SERVER'
            '</span>'
            '</div>', 
            unsafe_allow_html=True
        )
         files = [f for f in os.listdir(AUDIO_RAW_DIR) if not f.startswith('.')]
         selected_file = st.selectbox("", [""] + files, label_visibility="collapsed")

    action_file = None

    if uploaded_file:
        file_path = os.path.join(AUDIO_RAW_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        action_file = uploaded_file.name
        
        # Auto-Process Logic
        # We only auto-process if we haven't just processed this exact file to avoid loops on rerun
        if st.session_state.get("last_processed_file") != action_file:
            st.session_state.current_file = action_file
            st.success(f"✅ Securely Uploaded: {action_file}")
            st.toast("⚙️ Processing started automatically...", icon="🚀")
            
            # Mark as processed so we don't loop if user stays on page
            st.session_state.last_processed_file = action_file
            
            # Trigger Pipeline immediately
            process_pipeline(action_file)
            return # Stop further rendering to let pipeline take over
        else:
             # If we already processed it, just treat it as selected so user sees results/options
             st.session_state.current_file = action_file
        
    elif selected_file:
        action_file = selected_file
        st.session_state.current_file = action_file
        
    if action_file:
        base_name = os.path.splitext(action_file)[0]
        existing_json = os.path.join(SEGMENTS_DIR, f"{base_name}.json")
        
        # Selected File Card
        st.markdown(
            f'<div style="text-align: center; margin-top: 20px; padding: 20px; border-radius: 12px; background: rgba(108, 99, 255, 0.05); border: 1px solid var(--primary); animation: fadeIn 0.5s ease;">'
            f'<h3 style="margin: 0; color: var(--primary);">Selected: {action_file}</h3>'
            f'</div><br>',
            unsafe_allow_html=True
        )
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if os.path.exists(existing_json):
                st.info("✨ Analysis data exists for this file.")
                if st.button("👁️ View Insights Now", use_container_width=True):
                    st.session_state.page = "Timeline"
                    st.rerun()
                if st.button("🔄 Re-run Processor", use_container_width=True):
                    process_pipeline(action_file)
            else:
                if st.button("⚡ Start Processing Engine", type="primary", use_container_width=True):
                    process_pipeline(action_file)

def process_pipeline(filename):
    st.session_state.is_processing = True
    st.session_state.stop_requested = False
    
    st.write("---")
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### ⚙️ Pipeline Execution")
        status = st.status("Initializing...", expanded=True)
        p_bar = status.progress(0)
        
        try:
            # 0. Logger
            session_id, _ = SessionLogger.start_new_session()
            logger = SessionLogger.get_logger(__name__)
            logger.info(f"UI Triggered Processing for {filename}")
            
            raw_path = os.path.join(AUDIO_RAW_DIR, filename)
            
            # Helper to check stop
            def check_stop():
                if st.session_state.stop_requested:
                    status.update(label="🛑 Processing stopped by user.", state="error")
                    st.warning("Pipeline execution halted.")
                    st.session_state.is_processing = False
                    return True
                return False

            if check_stop(): return
            
            # 1. Preprocessing
            status.write("Cleaning Audio Signal...")
            processed_path = process_audio(raw_path, AUDIO_PROCESSED_DIR)
            p_bar.progress(20)
            
            if check_stop(): return
            
            # 2. Transcription

            status.write("Transcribing Content (Whisper) & Diarizing...")
            # Pass HF Token
            res = transcriber.process_file(processed_path, TRANSCRIPT_DIR, SEGMENTS_DIR, hf_token=st.session_state.hf_token)
            p_bar.progress(40)
            
            if check_stop(): return
            
            # 3. Segmentation
            status.write("Identifying Semantic Topics...")
            topics = segmenter.segment_transcript(res['segments'])
            p_bar.progress(60)
            
            if check_stop(): return
            
            # 4. Summarization
            status.write("Generating Condensed Summaries...")
            topics = summarizer.summarize_topics(topics)
            p_bar.progress(80)
            
            if check_stop(): return
            
            # 5. Keywords
            status.write("Extracting Key Terms...")
            topics = kw_extractor.extract_topics(topics)
            
            if check_stop(): return
            
            # 6. Emotion Analysis
            status.write("Analyzing Sentiment & Emotions...")
            topics = sentiment_agent.process_topics(topics)
            
            if check_stop(): return
            
            # Save
            base_name = os.path.splitext(filename)[0]
            s_path = os.path.join(SEGMENTS_DIR, f"{base_name}.json")
            with open(s_path, 'w', encoding='utf-8') as f:
                json.dump({"language": res.get('language'), "topics": topics}, f, indent=2, ensure_ascii=False)
            
            p_bar.progress(100)
            status.update(label="✅ Processing Complete!", state="complete", expanded=False)
            
            # Index immediately for search
            indexer.index_topics(topics)
            
            st.session_state.is_processing = False
            st.balloons()
            time.sleep(1)
            st.session_state.page = "Timeline" # Auto-redirect
            st.rerun()
            
        except Exception as e:
            st.session_state.is_processing = False
            status.update(label="❌ Failed", state="error")
            st.error(f"Pipeline Error: {e}")
            
            st.error(f"Pipeline Error: {e}")

@st.cache_data
def load_segments_data(json_path):
    """
    Cached data loader to prevent re-reading JSON from disk on every rerun.
    """
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
             return json.load(f)
    return None

def get_current_data():
    if not st.session_state.current_file:
        return None, None
        
    base_name = os.path.splitext(st.session_state.current_file)[0]
    s_path = os.path.join(SEGMENTS_DIR, f"{base_name}.json")
    
    data = load_segments_data(s_path)
    if data:
        return data, os.path.join(AUDIO_RAW_DIR, st.session_state.current_file)
    return None, None

def sync_indexer_if_needed(data):
    """
    Ensures the global indexer is loaded with the current file's topics.
    Crucial when switching files or reloading the page.
    """
    if not data or 'topics' not in data:
        return
        
    topics = data['topics']
    # Check if indexer needs update:
    # 1. Indexer has no topics
    # 2. Indexer has topics but count mismatch (simple heuristic)
    # 3. First topic ID mismatch (if IDs are unique/UUIDs, but here they are ints, so careful)
    # Better: Use session state to track indexed file
    
    current_file_ref = st.session_state.get('current_file', 'unknown')
    indexed_file_ref = st.session_state.get('indexed_file_ref', None)
    
    if indexed_file_ref != current_file_ref:
        # logger.info("Syncing Indexer with current data...")
        indexer.index_topics(topics)
        st.session_state.indexed_file_ref = current_file_ref

def render_timeline():
    data, audio_path = get_current_data()
    if not data:
        st.warning("No data available. Please Upload & Process a file first.")
        return
        
    # Sync Indexer (Optimization: Only re-indexes if file changed)
    sync_indexer_if_needed(data)
        
    topics = data.get('topics', [])
    st.markdown("<h2 style='color:var(--text-primary); margin-bottom:20px;'>⏳ Topic Timeline</h2>", unsafe_allow_html=True)
    
    # Styled Metrics
    total_dur = topics[-1]['end'] - topics[0]['start']
    c1, c2 = st.columns(2)
    c1.markdown(f"""<div class="metric-card"><h4>Total Duration</h4><h2 style="color:var(--primary);">{total_dur/60:.1f} min</h2></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><h4>Topic Segments</h4><h2 style="color:var(--primary);">{len(topics)}</h2></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Visual
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        df = pd.DataFrame(topics)
        df['duration'] = df['end'] - df['start']
        df['label'] = df.apply(lambda x: x.get('title', f"Topic {x['id']}"), axis=1)
        df['summary_short'] = df['summary'].apply(lambda x: x[:60] + "..." if x else "")
        
        fig = px.bar(
            df, 
            x='duration', 
            y='id', 
            orientation='h',
            text='label',
            hover_data=['summary_short'],
            color='duration',
            color_continuous_scale='Plasma'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#1A1A40',
            height=500,
            xaxis=dict(showgrid=True, gridcolor='rgba(108, 99, 255, 0.1)', title="Duration (s)"),
            yaxis=dict(autorange="reversed", title="Sequence"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    render_emotion_flow(topics)

def render_emotion_flow(topics):
    st.markdown("<h3 style='color:var(--text-primary); margin-top:40px;'>🎭 Speaker–Emotion Flow Timeline</h3>", unsafe_allow_html=True)
    
    if not topics:
        st.info("No topic data available.")
        return

    # Prepare Data
    data = []
    # Prepare Data
    data = []
    
    for t in topics:
        # Determine source items: use granular segments if available, else topic fallback
        if 'segments' in t and t['segments']:
            source_items = t['segments']
        else:
            source_items = [t]
            
        for item in source_items:
            if 'emotion' not in item or 'start' not in item:
                 continue
                 
            # Time point (midpoint of segment)
            midpoint = (item['start'] + item['end']) / 2 / 60 # minutes
            duration = item['end'] - item['start']
            
            # Emotion Intensity
            score = item.get('emotion_score', 0)
            # Use raw score for intensity or weight by duration? 
            # Weighted by duration makes short segments less visible, which might be good for noise,
            # but we want to see bursts. Let's keep existing logic: score * duration.
            intensity = score * duration
            
            # Speaker
            speaker = item.get('speaker', 'Speaker 1')
            
            data.append({
                "Time (min)": midpoint,
                "Intensity": intensity,
                "Emotion": item.get('emotion', 'neutral'),
                "Speaker": speaker,
                "Summary": t.get('summary', '')[:60] + "...", # Topic summary context
                "Text": item.get('text', '')[:60] + "..."
            })
        
    if not data:
         st.warning("No emotion data found in topics.")
         return

    df = pd.DataFrame(data)
    
    # Filter Controls inside a card
    with st.container():
        st.markdown('<div class="glass-card" style="padding: 15px;">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            all_speakers = list(df['Speaker'].unique())
            selected_speakers = st.multiselect("Filter Speakers", options=all_speakers, default=all_speakers)
        with c2:
            all_emotions = list(df['Emotion'].unique())
            selected_emotions = st.multiselect("Filter Emotions", options=all_emotions, default=all_emotions)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if not selected_speakers or not selected_emotions:
        st.warning("Please select at least one speaker and emotion.")
        return
        
    filtered_df = df[df['Speaker'].isin(selected_speakers) & df['Emotion'].isin(selected_emotions)]
    
    if filtered_df.empty:
        st.warning("No data matches the filters.")
        return

    # Plotly Chart
    color_map = {
        "joy": "#FFD700",
        "anger": "#FF4500",
        "sadness": "#1E90FF",
        "fear": "#8B008B",
        "disgust": "#556B2F",
        "neutral": "#A9A9A9"
    }
    
    # We sort by Time to ensure lines connect properly
    filtered_df = filtered_df.sort_values(by="Time (min)")
    
    fig = px.line(
        filtered_df, 
        x="Time (min)", 
        y="Intensity", 
        color="Emotion",
        symbol="Speaker",
        line_shape="spline",
        render_mode="svg", # better for curved lines
        color_discrete_map=color_map,
        hover_data=["Speaker", "Summary", "Text"],
        markers=True
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1A1A40',
        height=450,
        xaxis_title="Time (minutes)",
        yaxis_title="Emotion Intensity (Score × Duration)",
        hovermode="x unified"
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Emotion Flow CSV",
        data=csv,
        file_name=f"emotion_flow.csv",
        mime="text/csv"
    )

def render_transcription():
    data, _ = get_current_data()
    if not data:
        st.warning("No data available.")
        return
    
    topics = data.get('topics', [])
    st.markdown("<h2 style='color:var(--text-primary); margin-bottom:20px;'>📝 Full Transcript</h2>", unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        full_text = "\n\n".join([t.get('text', '') for t in topics])
        st.markdown(f"""
<div class="glass-card" style="height: 600px; overflow-y: scroll;">
<div style="font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--text-secondary); white-space: pre-wrap;">
{full_text}
</div>
</div>
""", unsafe_allow_html=True)

    with col_side:
        st.markdown("""
<div class="glass-card">
<h4 style="color:var(--primary);">Key Actions</h4>
<hr style="border-top: 1px solid var(--border-color);">
<p>🔍 <b>Search</b></p>
</div>
""", unsafe_allow_html=True)
        search = st.text_input("Find in transcript...", placeholder="Enter keyword...")
        if search:
            # PURE SAFETY: Ensure index exists for these topics
            # If the app reloaded, 'indexer' might be fresh and empty
            if not indexer.topics or len(indexer.topics) == 0:
                 # We need to re-index quietly
                 indexer.index_topics(topics)

            # 1. Search Logic: Use Semantic Indexer
            semantic_results = indexer.search(search, top_n=5)
            
            # Convert to local format matching segments list
            # We want to use the full topic object but adding the score
            matching_segments = []
            for res in semantic_results:
                original_topic = indexer.get_topic_by_id(res['id'])
                if original_topic:
                    # Create a copy to not mutate original
                    t_copy = original_topic.copy() 
                    t_copy['search_score'] = res.get('score', 0)
                    matching_segments.append(t_copy)
            
            if matching_segments:
                # Auto-Scroll Logic: Trigger only on new search
                first_match_id = matching_segments[0]['id']
                if search != st.session_state.get('last_search'):
                    st.session_state.last_search = search
                    # Inject JS to jump hash
                    st.markdown(
                        f"<script>location.hash = 'segment-{first_match_id}';</script>", 
                        unsafe_allow_html=True
                    )
                
                st.markdown(f"<div style='margin-top:10px; margin-bottom:10px; font-size:0.9em;'><b>🔍 Semantic Results for:</b> <span style='color:var(--primary);'>{search}</span> — Top {len(matching_segments)} matches</div>", unsafe_allow_html=True)
                
                for t in matching_segments:
                    # Timestamp Format
                    start_sec = int(t['start'])
                    ts_fmt = f"{start_sec//60}:{start_sec%60:02d}"
                    title = t.get('title', f"Topic {t['id']}")
                    score = t.get('search_score', 0)
                    
                    # 3. Highlighting using Indexer
                    styled_text = indexer.highlight_text(t.get('text', ''), search)
                    
                    # Add Score Badge
                    with st.expander(f"🧩 {ts_fmt} | {title} (Relevance: {score:.2f})"):
                        st.markdown(f"<div style='font-size:0.85rem; line-height:1.6;'>{styled_text}</div>", unsafe_allow_html=True)
            else:
                st.warning("No segments contain that keyword.")
            
    st.markdown("---")
    render_segments()
    # Chatbot is now floating, called at the end
    render_floating_chatbot()

def render_floating_chatbot():
    # 1. State Management
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False

    # 2. CSS for Floating UI
    st.markdown("""
    <style>
        /* Simpler, Direct Target for the Popover Container */
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            z-index: 2147483647 !important; /* Max Z-Index */
            display: block !important;
            width: auto !important;
            height: auto !important;
            transform: none !important; /* Prevent parent transforms from affecting fixed pos */
        }

        /* Styling the button inside */
        div[data-testid="stPopover"] button {
            width: 60px !important;
            height: 60px !important;
            border-radius: 50% !important;
            background-color: #6C63FF !important;
            color: white !important;
            border: none !important;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 3. Floating Button Implementation via Streamlit Popover
    try:
        # Use an Emoji as the label for the round button
        with st.popover("💬", help="Chat with the podcast"):
            st.markdown("### 🤖 Podcast Assistant")
            
            # Context Reset Logic
            if "chat_file" not in st.session_state:
                st.session_state.chat_file = st.session_state.current_file
                st.session_state.chat_history = []
            elif st.session_state.chat_file != st.session_state.current_file:
                st.session_state.chat_file = st.session_state.current_file
                st.session_state.chat_history = []

            # Chat History
            messages_container = st.container(height=400)
            with messages_container:
                 for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            
            # Input
            if query := st.chat_input("Ask a question...", key="float_chat_input"):
                st.session_state.chat_history.append({"role": "user", "content": query})
                with messages_container:
                     with st.chat_message("user"):
                        st.markdown(query)
                     
                     with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            # Hydrate Indexer if needed
                            data, _ = get_current_data()
                            sync_indexer_if_needed(data)
                                
                            response = chatbot.ask(query, indexer)
                            answer = response.get('answer', "I don't know.")
                            refs = response.get('references', [])
                            
                            full_text = answer
                            if refs:
                                full_text += "\n\n**Sources:**\n" + "\n".join([f"- {r}" for r in refs])
                            
                            st.markdown(full_text)
                            st.session_state.chat_history.append({"role": "assistant", "content": full_text})
                            
    except AttributeError:
        # Fallback for older Streamlit: Use a sidebar or simple expander at bottom
        with st.expander("💬 Ask AI Assistant (Pop-up)", expanded=False):
             # Copy of logic above...
             st.warning("Please upgrade Streamlit to use the floating popover!")
             # (Simplified fallback logic same as above)


def render_segments():
    data, audio_path = get_current_data()
    if not data:
        st.warning("No data available.")
        return
        
    topics = data.get('topics', [])
    st.header("🧩 Topic Analysis")
    
    # Global audio load
    full_audio = None
    if audio_path and os.path.exists(audio_path):
        full_audio = load_audio_file(audio_path)
        
    for t in topics:
        title = t.get('title', f"Topic {t['id']}")
        start_fmt = str(timedelta(seconds=int(t['start'])))
        
        # Anchor for Auto-Scroll
        st.markdown(f"<div id='segment-{t['id']}'></div>", unsafe_allow_html=True)
        
        with st.expander(f"📌 {start_fmt} | {title}", expanded=False):
            # Keywords
            kws = t.get('keywords', [])
            if kws:
                html = "".join([f"<span class='tag'>{k}</span>" for k in kws])
                st.markdown(f"<div style='margin-bottom:12px;'>{html}</div>", unsafe_allow_html=True)

            # Summary
            st.markdown(f"**Summary:** {t.get('summary', 'No summary')}")
            
            # Sentiment Badge (Below Summary)
            sent = t.get('sentiment', 'NEUTRAL').upper()
            s_color = "#00E676" if sent == 'POSITIVE' else "#FF2E63" if sent == 'NEGATIVE' else "#A9A9A9"
            st.markdown(f"<div style='margin-top:10px; margin-bottom:10px;'><b>Sentiment:</b> <span style='background:{s_color}; color:white; padding:2px 8px; border-radius:10px; font-size:0.8em; font-weight:bold;'>{sent}</span></div>", unsafe_allow_html=True)
            
            # Bullets
            if t.get('bullets'):
                 st.markdown("**Key Points:**")
                 for b in t['bullets']:
                     st.markdown(f"- {b}")

            st.markdown("---")
            st.markdown("**Transcript:**")
            st.text(t.get('text', ''))
            
            # Audio Playback
            if full_audio:
                s = int(t['start'] * 1000)
                e = int(t['end'] * 1000)
                if e > len(full_audio): e = len(full_audio)
                if s < e:
                    cur_audio = full_audio[s:e]
                    buf = io.BytesIO()
                    cur_audio.export(buf, format="mp3")
                    st.audio(buf, format="audio/mp3")





# --- MAIN ROUTER ---

def main():
    if st.session_state.page != "Home":
        render_navbar()
    
    page = st.session_state.page
    
    if page == "Home":
        render_home()
    elif page == "Upload":
        render_upload()
    elif page == "Timeline":
        render_timeline()
    elif page == "Transcription":
        render_transcription()

    
    # Sidebar footer style if it appears
    st.markdown("<footer><center style='color:#374151; margin-top:50px;'>Podcast Intelligence Engine v2.0</center></footer>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
