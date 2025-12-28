import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import soundfile as sf
import io
import re
import numpy as np 
from textblob import TextBlob
from datetime import datetime, timedelta

# --- 1. PAGE CONFIGURATION ---
def setup_page():
    st.set_page_config(
        page_title="Podcast Intelligence Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# --- 2. PROFESSIONAL STYLING ---
def apply_custom_styling():
    st.markdown("""
    <style>
    /* App Background */
    .stApp { background-color: #ffffff; }
    
    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] { background-color: #2c3e50; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { 
        color: #ffffff !important; 
    }
    [data-testid="stSidebar"] label[data-testid="stLabel"] {
        color: #ffffff !important; font-weight: bold;
    }
    
    /* Info Box Fix */
    [data-testid="stSidebar"] .stAlert { background-color: #e1f5fe !important; }
    [data-testid="stSidebar"] .stAlert p { color: #0d47a1 !important; }
    
    /* Status Text */
    [data-testid="stSidebar"] [data-testid="stText"] { color: #2ecc71 !important; font-weight: bold; }

    /* Dropdown Fix */
    div[data-baseweb="select"] > div { color: #2c3e50; background-color: #ffffff; }
    div[data-baseweb="menu"] div { color: #2c3e50 !important; }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(to right, #2196F3, #1976D2);
        color: white; border: none; padding: 10px 24px; border-radius: 50px;
        font-weight: 600; width: 100%; transition: 0.3s;
    }
    div.stButton > button:hover {
        background: linear-gradient(to right, #1976D2, #1565C0);
        box-shadow: 0 4px 10px rgba(33, 150, 243, 0.3);
    }
    
    /* Keywords */
    .keyword-badge {
        background-color: #E3F2FD; color: #1565C0; padding: 5px 12px;
        border-radius: 20px; font-weight: 500; font-size: 0.9em;
        margin-right: 6px; border: 1px solid #BBDEFB; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def seconds_to_datetime(seconds):
    return datetime(2024, 1, 1) + timedelta(seconds=seconds)

def extract_audio_segment(full_audio_path, start_sec, end_sec):
    try:
        data, samplerate = sf.read(full_audio_path)
        start_sample = int(start_sec * samplerate)
        end_sample = int(end_sec * samplerate)
        if end_sample > len(data): end_sample = len(data)
        segment_data = data[start_sample:end_sample]
        if len(segment_data) < samplerate * 0.5: return None
        buffer = io.BytesIO()
        sf.write(buffer, segment_data, samplerate, format='WAV')
        buffer.seek(0)
        return buffer
    except Exception as e:
        return None

# --- NEW: COLLISION-FREE PACKING ALGORITHM ---
def get_bubble_placement(keywords_data):
    """
    Calculates x, y coordinates for bubbles so they DO NOT OVERLAP.
    Uses a greedy search algorithm.
    """
    if not keywords_data:
        return pd.DataFrame()

    df = pd.DataFrame(keywords_data)
    # Define radius proportional to count (sqrt ensures area is proportional)
    # We multiply by a factor to get a reasonable "simulation radius"
    df['r'] = np.sqrt(df['count']) 
    
    # Store placed bubbles: {'x': 0, 'y': 0, 'r': 5}
    placed_bubbles = []
    
    coords = []
    
    # Sort by size descending (place biggest first)
    df = df.sort_values('count', ascending=False).reset_index(drop=True)

    for i, row in df.iterrows():
        r = row['r']
        
        # First bubble goes in the exact center
        if i == 0:
            placed_bubbles.append({'x': 0, 'y': 0, 'r': r})
            coords.append({'x': 0, 'y': 0})
            continue

        # For subsequent bubbles, search for a spot
        # We start searching closely around the center and spiral out
        found_spot = False
        angle_step = 0.5 # Radians
        search_radius = 0.1 # Start close
        
        while not found_spot:
            # Check points along a circle at current search_radius
            theta = 0
            while theta < 2 * np.pi:
                # Potential coordinates
                x = search_radius * np.cos(theta)
                y = search_radius * np.sin(theta)
                
                # Check collision with ALL previously placed bubbles
                collision = False
                for b in placed_bubbles:
                    # Calculate distance between centers
                    dist = np.sqrt((x - b['x'])**2 + (y - b['y'])**2)
                    # Check if they overlap (Distance must be >= sum of radii)
                    # We add a tiny buffer (1.1x) for visual spacing
                    if dist < (r + b['r']) * 1.1:
                        collision = True
                        break
                
                if not collision:
                    placed_bubbles.append({'x': x, 'y': y, 'r': r})
                    coords.append({'x': x, 'y': y})
                    found_spot = True
                    break
                
                theta += angle_step
            
            # If we went around the whole circle and didn't find a spot, move further out
            search_radius += 0.5 # Increase search distance
            
            # Safety break to prevent infinite loops
            if search_radius > 100:
                coords.append({'x': search_radius, 'y': 0}) # Just put it far away
                break

    # Add coordinates back to dataframe
    coords_df = pd.DataFrame(coords)
    df['x'] = coords_df['x']
    df['y'] = coords_df['y']
    
    return df

# --- 4. MAIN APPLICATION ---
def main():
    setup_page()
    apply_custom_styling()

    # --- Sidebar ---
    with st.sidebar:
        st.header("Settings")
        model_size = st.selectbox("Transcription Model", ["base", "tiny", "small"], index=1)
        st.info("💡 **Note:** 'Tiny' is fastest. 'Base' is most accurate.")
        st.markdown("---")
        st.text("Status: Online 🟢")

    # --- Header ---
    st.title("Automated Podcast Intelligence")
    st.markdown("Upload audio to generate structured transcripts, topic bubbles, and semantic search.")

    # --- Upload ---
    uploaded_file = st.file_uploader("Upload Audio File (MP3, WAV)", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        st.markdown("---")
        with st.expander("🎧 Preview Original Audio"):
            st.audio(uploaded_file, format='audio/wav')

        if st.button("Initialize Processing Pipeline"):
            try:
                from preprocessing import clean_audio
                from transcription import transcribe_audio
                from segmentation import segment_transcript
                from keyword_extraction import get_global_keyword_counts
            except ImportError as e:
                st.error(f"System Error: Backend modules missing. {e}")
                st.stop()

            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # 1. Ingestion
                status_text.text("Phase 1/4: Ingesting file...")
                with open("temp_input.wav", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                progress_bar.progress(10)

                # 2. Cleaning
                status_text.text("Phase 2/4: Optimizing audio quality...")
                cleaned_path = clean_audio("temp_input.wav")
                progress_bar.progress(30)

                # 3. Transcription
                status_text.text(f"Phase 3/4: Transcribing ({model_size})...")
                transcript_text = transcribe_audio(cleaned_path, model_size=model_size)
                
                if not transcript_text:
                    st.error("Transcription failed.")
                    st.stop()
                progress_bar.progress(60)

                # 4. Intelligence
                status_text.text("Phase 4/4: Generating segments and bubble analytics...")
                segments = segment_transcript(transcript_text)
                global_keywords = get_global_keyword_counts(transcript_text, top_n=35)
                
                progress_bar.progress(100)
                status_text.success("Analysis Complete.")

                st.session_state['data'] = {
                    'segments': segments,
                    'transcript': transcript_text,
                    'cleaned_path': cleaned_path,
                    'global_keywords': global_keywords
                }

            except Exception as e:
                st.error(f"Processing Error: {e}")
            finally:
                if os.path.exists("temp_input.wav"):
                    os.remove("temp_input.wav")

    # --- 5. DASHBOARD RENDERING ---
    if 'data' in st.session_state:
        data = st.session_state['data']
        segments = data['segments']
        global_keywords = data['global_keywords']
        cleaned_path = data['cleaned_path']
        
        df = pd.DataFrame(segments)
        if not df.empty:
            df["start_dt"] = df["start"].apply(seconds_to_datetime)
            df["end_dt"] = df["end"].apply(seconds_to_datetime)
            df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

        tab_bubbles, tab_timeline, tab_search, tab_raw = st.tabs([
            "Keyword Bubbles", "Topic Timeline", "Search & Play", "Transcript"
        ])

        # --- TAB 1: BUBBLES (COLLISION-FREE) ---
        with tab_bubbles:
            st.subheader("Top Topics")
            st.markdown("Topics sized by frequency.")
            
            if global_keywords and len(global_keywords) > 2:
                # USE NEW PLACEMENT ALGORITHM
                df_kw = get_bubble_placement(global_keywords)
                
                # Plotly Scatter
                fig = px.scatter(
                    df_kw, x="x", y="y", size="count", text="keyword",
                    size_max=100, hover_name="keyword",
                    hover_data={"x": False, "y": False, "count": True}
                )
                
                # Style: Solid Blue, White Text
                fig.update_traces(
                    marker=dict(color='#1E88E5', opacity=1.0, line=dict(width=0)),
                    textposition='middle center',
                    textfont=dict(color='white', family="Arial Black")
                )
                
                # Hide Axes completely
                fig.update_layout(
                    xaxis=dict(showgrid=False, zeroline=False, visible=False),
                    yaxis=dict(showgrid=False, zeroline=False, visible=False),
                    plot_bgcolor='white', height=650, margin=dict(l=0, r=0, t=20, b=0),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough distinct keywords found.")

        # --- TAB 2: TIMELINE ---
        with tab_timeline:
            st.subheader("Conversation Flow")
            if not df.empty:
                fig_tl = px.timeline(
                    df, x_start="start_dt", x_end="end_dt", y="topic", color="sentiment",
                    color_continuous_scale=["#ef5350", "#e0e0e0", "#66bb6a"],
                    title="Timeline Analysis"
                )
                fig_tl.update_xaxes(tickformat="%M:%S")
                fig_tl.update_yaxes(autorange="reversed")
                st.plotly_chart(fig_tl, use_container_width=True)

        # --- TAB 3: SEARCH ---
        with tab_search:
            st.subheader("Deep Search")
            col_search, col_filt = st.columns([3, 1])
            with col_search:
                query = st.text_input("Search Topic:", placeholder="e.g. money")
            with col_filt:
                sent_filter = st.slider("Min Sentiment", -1.0, 1.0, -1.0)

            if not df.empty:
                results = df
                if query:
                    mask = results.apply(lambda row: any(query.lower() in k.lower() for k in row['keywords']), axis=1)
                    results = results[mask]
                results = results[results['sentiment'] >= sent_filter]

                st.markdown(f"**Found {len(results)} matches:**")
                
                for idx, row in results.iterrows():
                    start_str = f"{int(row['start']//60):02d}:{int(row['start']%60):02d}"
                    end_str = f"{int(row['end']//60):02d}:{int(row['end']%60):02d}"
                    
                    with st.expander(f"▶️ {start_str} - {end_str} | {row['topic']}"):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            kw_html = "".join([f"<span class='keyword-badge'>{k}</span>" for k in row['keywords']])
                            st.markdown(kw_html, unsafe_allow_html=True)
                            st.markdown("---")
                            st.markdown(f"**Summary:** {row['summary']}")
                            st.markdown(f"> {row['text']}")
                        with c2:
                            st.markdown("**Playback**")
                            audio_bytes = extract_audio_segment(cleaned_path, row['start'], row['end'])
                            if audio_bytes:
                                st.audio(audio_bytes, format='audio/wav')

        # --- TAB 4: RAW ---
        with tab_raw:
            st.text_area("Full Transcript", data['transcript'], height=450)

if __name__ == "__main__":
    main()