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

# --- 2. ADVANCED STYLING ---
def apply_custom_styling():
    st.markdown("""
    <style>
    /* IMPORT GOOGLE FONT */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* MAIN BACKGROUND GRADIENT */
    .stApp {
        background: linear-gradient(to bottom right, #f0f4f8, #d9e2ec);
    }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #102a43; /* Navy Blue */
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    }
    
    /* SIDEBAR TEXT COLORS */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f0f4f8 !important;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
        color: #bcccdc !important;
    }
    
    /* HEADER STYLING */
    h1 {
        color: #102a43;
        font-weight: 700;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #243b53;
        font-weight: 600;
    }

    /* BUTTON STYLING */
    div.stButton > button {
        background: linear-gradient(90deg, #334E68 0%, #102a43 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(16, 42, 67, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(16, 42, 67, 0.3);
        background: linear-gradient(90deg, #486581 0%, #243b53 100%);
        color: white;
    }
    
    /* KEYWORD BADGES */
    .keyword-badge {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 2px;
        display: inline-block;
        border: 1px solid #bbdefb;
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

# --- IMPROVED BUBBLE PLACEMENT (SPIRAL PACKING) ---
def get_bubble_placement(keywords_data):
    """
    Improved collision avoidance using a Spiral Search algorithm.
    This forces bubbles to spread out so they don't overlap.
    """
    if not keywords_data:
        return pd.DataFrame()

    df = pd.DataFrame(keywords_data)
    # Scale radius for visibility
    df['r'] = np.sqrt(df['count']) * 1.5 
    
    # Sort: Largest bubbles in the middle
    df = df.sort_values('count', ascending=False).reset_index(drop=True)
    
    placed_bubbles = [] # List of {'x', 'y', 'r'}
    coords = []

    for i, row in df.iterrows():
        r = row['r']
        
        # First bubble goes exactly in center
        if i == 0:
            placed_bubbles.append({'x': 0, 'y': 0, 'r': r})
            coords.append({'x': 0, 'y': 0})
            continue

        # For subsequent bubbles, spiral out from center until space is found
        # Spiral Equation: x = (a + b*angle) * cos(angle), y = (a + b*angle) * sin(angle)
        angle = 0.0
        step = 0.5 # Step size for angle
        found = False
        
        # Limit search to avoid infinite loop
        while angle < 100: 
            dist = 1.0 * angle # Distance from center grows with angle
            x = dist * np.cos(angle)
            y = dist * np.sin(angle)
            
            # Check collision with ALL previously placed bubbles
            collision = False
            for b in placed_bubbles:
                # Euclidean distance
                d = np.sqrt((x - b['x'])**2 + (y - b['y'])**2)
                
                # Check overlap: Distance must be > (radius1 + radius2) + padding
                if d < (r + b['r']) * 1.1: 
                    collision = True
                    break
            
            if not collision:
                placed_bubbles.append({'x': x, 'y': y, 'r': r})
                coords.append({'x': x, 'y': y})
                found = True
                break
            
            angle += 0.2 # Increase angle to spiral out

        # If no spot found (rare), just place it far out
        if not found:
            coords.append({'x': i * 5, 'y': 0})

    coords_df = pd.DataFrame(coords)
    df['x'] = coords_df['x']
    df['y'] = coords_df['y']
    return df

# --- 4. MAIN APPLICATION ---
def main():
    setup_page()
    apply_custom_styling()

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Dashboard Settings")
        st.markdown("---")
        model_size = st.selectbox(
            "Transcription Model", 
            ["base", "tiny", "small"], 
            index=1,
            help="Select 'Tiny' for speed or 'Base' for accuracy."
        )
        st.info("💡 **Tip:** Upload clear audio for best results.")
        st.markdown("---")
        
        # Placeholder for Sidebar Download Button
        download_placeholder = st.empty()
        
        st.caption("v1.0 • Built with Whisper & Streamlit")

    # --- MAIN CONTENT ---
    st.markdown("# 🎙️ Podcast Intelligence Hub")
    st.markdown("### Transform your audio into searchable, structured insights.")
    st.markdown("---")

    with st.container():
        uploaded_file = st.file_uploader("📂 Upload Audio File (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🎧 Audio Preview")
            st.audio(uploaded_file, format='audio/wav')
            
        with col2:
            st.markdown("#### 🚀 Analysis")
            process_btn = st.button("Start AI Processing", type="primary")

        if process_btn:
            try:
                # Backend imports
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
                status_text.markdown("**Phase 1/4:** 📥 Ingesting file...")
                with open("temp_input.wav", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                progress_bar.progress(10)

                # 2. Cleaning
                status_text.markdown("**Phase 2/4:** 🧹 Cleaning audio signal...")
                cleaned_path = clean_audio("temp_input.wav")
                progress_bar.progress(30)

                # 3. Transcription
                status_text.markdown(f"**Phase 3/4:** 📝 Transcribing with Whisper ({model_size})...")
                transcript_text = transcribe_audio(cleaned_path, model_size=model_size)
                
                if not transcript_text:
                    st.error("Transcription returned empty text.")
                    st.stop()
                progress_bar.progress(60)

                # 4. Intelligence
                status_text.markdown("**Phase 4/4:** 🧠 Analyzing topics & keywords...")
                segments = segment_transcript(transcript_text)
                global_keywords = get_global_keyword_counts(transcript_text, top_n=35)
                
                progress_bar.progress(100)
                status_text.success("✅ Processing Complete!")

                # Store data in session state
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
        st.markdown("---")
        data = st.session_state['data']
        segments = data['segments']
        global_keywords = data['global_keywords']
        cleaned_path = data['cleaned_path']
        transcript_text = data['transcript']
        
        # --- SIDEBAR DOWNLOAD BUTTON ---
        with download_placeholder:
             st.download_button(
                label="📥 Download Full Transcript",
                data=transcript_text,
                file_name="podcast_transcript.txt",
                mime="text/plain",
                key="sidebar_dl"
            )

        df = pd.DataFrame(segments)
        if not df.empty:
            df["start_dt"] = df["start"].apply(seconds_to_datetime)
            df["end_dt"] = df["end"].apply(seconds_to_datetime)
            df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

        # TABS
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔮 Keyword Bubbles", "📈 Topic Timeline", "🔍 Search & Play", "📄 Full Transcript"
        ])

        # TAB 1: BUBBLES
        with tab1:
            st.markdown("### ☁️ Discussion Themes")
            if global_keywords and len(global_keywords) > 2:
                df_kw = get_bubble_placement(global_keywords)
                
                # Plotly Bubble Chart
                fig = px.scatter(
                    df_kw, 
                    x="x", 
                    y="y", 
                    size="count", 
                    text="keyword",
                    size_max=80, 
                    hover_name="keyword",
                    hover_data={"x": False, "y": False, "count": True}
                )
                
                # FIXED: UNIFORM COLOR & REMOVED OVERLAP
                fig.update_traces(
                    marker=dict(
                        color='#1E88E5',  # SOLID CORPORATE BLUE
                        opacity=0.9, 
                        line=dict(width=1, color='white')
                    ),
                    textposition='middle center',
                    textfont=dict(color='white', family="Poppins", weight="bold", size=11)
                )
                
                fig.update_layout(
                    xaxis=dict(visible=False, showgrid=False, zeroline=False), 
                    yaxis=dict(visible=False, showgrid=False, zeroline=False),
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=600, 
                    showlegend=False,
                    margin=dict(t=20, b=20, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough data to generate keywords.")

        # TAB 2: TIMELINE
        with tab2:
            st.markdown("### ⏱️ Topic Progression")
            if not df.empty:
                fig_tl = px.timeline(
                    df, x_start="start_dt", x_end="end_dt", y="topic", color="sentiment",
                    color_continuous_scale="RdBu", title="Sentiment Heatmap"
                )
                fig_tl.update_yaxes(autorange="reversed")
                fig_tl.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_tl, use_container_width=True)

        # TAB 3: SEARCH
        with tab3:
            st.markdown("### 🔎 Semantic Search")
            col_search, col_filt = st.columns([3, 1])
            with col_search:
                query = st.text_input("Search for a concept:", placeholder="e.g. 'Future technology'")
            with col_filt:
                sent_filter = st.slider("Min Sentiment Score", -1.0, 1.0, -1.0)

            if not df.empty:
                results = df
                if query:
                    mask = results.apply(lambda row: any(query.lower() in k.lower() for k in row['keywords']), axis=1)
                    results = results[mask]
                results = results[results['sentiment'] >= sent_filter]

                st.info(f"Found **{len(results)}** segments matching your search.")
                
                for idx, row in results.iterrows():
                    start_str = f"{int(row['start']//60):02d}:{int(row['start']%60):02d}"
                    with st.expander(f"▶️ {start_str} | {row['topic']}"):
                        col_txt, col_audio = st.columns([3, 1])
                        with col_txt:
                            kw_html = "".join([f"<span class='keyword-badge'>{k}</span>" for k in row['keywords']])
                            st.markdown(kw_html, unsafe_allow_html=True)
                            st.markdown(f"**Summary:** {row['summary']}")
                            st.caption(f"\"{row['text']}\"")
                        with col_audio:
                            st.markdown("**Listen**")
                            audio_bytes = extract_audio_segment(cleaned_path, row['start'], row['end'])
                            if audio_bytes:
                                st.audio(audio_bytes, format='audio/wav')

        # TAB 4: RAW TRANSCRIPT
        with tab4:
            st.markdown("### 📝 Raw Text")
            st.text_area("Full Transcript", data['transcript'], height=500)
            
            # Tab Download Button
            st.download_button(
                label="📥 Download TXT",
                data=transcript_text,
                file_name="transcript_full.txt",
                mime="text/plain",
                key="tab_dl"
            )

if __name__ == "__main__":
    main()