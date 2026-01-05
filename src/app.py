import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import re
import time
import unittest
import io
import sys
from pathlib import Path


import podcast_backend


CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent / "podcast_data"
TESTS_DIR = CURRENT_DIR.parent / "tests"


TRANSCRIPT_DIR = BASE_DIR / "transcripts"
SUMMARY_DIR = BASE_DIR / "short_summary"
TOPIC_DIR = BASE_DIR / "semantic_segments"
KEYWORD_DIR = BASE_DIR / "keywords"
SENTIMENT_DIR = BASE_DIR / "sentiment_data"


st.set_page_config(
    page_title="Podcast AI Analytics",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem; }
    .metric-card { background-color: #F3F4F6; color: #1F2937; padding: 1rem; border-radius: 8px; border-left: 5px solid #4F46E5; margin-bottom: 1rem; }
    .highlight { background-color: #FEF3C7; color: #000000; padding: 0.1rem 0.3rem; border-radius: 4px; font-weight: 500; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; border-radius: 4px 4px 0 0; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
    .test-output { background-color: #1e1e1e; color: #d4d4d4; padding: 1rem; border-radius: 8px; font-family: monospace; white-space: pre-wrap; }
    
    /* Sentiment Colors */
    .sentiment-positive { color: #10B981; font-weight: bold; }
    .sentiment-negative { color: #EF4444; font-weight: bold; }
    .sentiment-neutral { color: #6B7280; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">🎙️ AI Podcast Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Transcription, Segmentation, Sentiment Analysis, and Summarization.</div>', unsafe_allow_html=True)

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    st.subheader("1. Add Content")
    input_tab1, input_tab2 = st.tabs(["📤 Upload", "🔗 URL"])
    
    uploaded_file = None
    audio_url = ""
    
    with input_tab1:
        uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a", "flac"])
    with input_tab2:
        audio_url = st.text_input("Paste Audio URL", placeholder="https://example.com/episode.mp3")

    st.divider()

    st.subheader("2. Analysis Features")
    language = st.selectbox("Audio Language", ["English", "Spanish", "French", "German", "Hindi", "Japanese"])
    translate_opt = st.checkbox("Translate to English", value=False)

    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("Sentiment Analysis", value=True)
    with c2:
        st.checkbox("Topic Segmentation", value=True)
        
    st.divider()
    
    if st.button("🚀 Start Processing", type="primary", use_container_width=True):
        source = uploaded_file if uploaded_file else audio_url
        is_url = bool(audio_url) and not uploaded_file
        
        if source:
            with st.spinner("🤖 AI is working... This may take a few minutes."):
                try:
                   
                    status = podcast_backend.process_new_upload(source, str(BASE_DIR), is_url=is_url)
                    if status == "Success":
                        st.success("✅ Done! Refreshing...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error: {status}")
                except Exception as e:
                    st.error(f"Critical Error: {str(e)}")
        else:
            st.warning("Please upload a file or paste a link.")

    st.divider()
    st.subheader("🔎 Search Archive")
    search_query = st.text_input("Filter podcasts by keyword:", placeholder="e.g. climate, tech...")


def get_file_list(query):
    if not os.path.exists(TRANSCRIPT_DIR): return []
    files = [f.replace(".json", "") for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".json")]
    if not query: return files
    
    matches = []
    query = query.lower()
    for f in files:
        t_path = TRANSCRIPT_DIR / f"{f}.json"
        k_path = KEYWORD_DIR / f"{f}_keywords.txt"
        found = False
        if t_path.exists():
            try:
                if query in json.loads(t_path.read_text(encoding='utf-8')).get('text', '').lower(): found = True
            except: pass
        if not found and k_path.exists():
            try:
                if query in k_path.read_text(encoding='utf-8').lower(): found = True
            except: pass
        if found: matches.append(f)
    return matches

def load_data(folder, filename, is_json=False):
    path = Path(folder) / filename
    if path.exists():
        text = path.read_text(encoding='utf-8')
        return json.loads(text) if is_json else text
    return None

def time_to_seconds(time_str):
    """Converts MM:SS to seconds (int)"""
    try:
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        return 0
    return 0

def parse_topics(raw_text):
    """Parses Topic File into Structured Data with Timestamps"""
    topics = []
    current_topic = {}
    lines = raw_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        
        header_match = re.match(r"🔹 TOPIC \d+\s+\[(.*?)\s+-\s+(.*?)\]:\s+(.*)", line)
        
        if header_match:
            if current_topic: topics.append(current_topic)
            current_topic = {
                "start_str": header_match.group(1),
                "end_str": header_match.group(2),
                "start_sec": time_to_seconds(header_match.group(1)),
                "end_sec": time_to_seconds(header_match.group(2)),
                "title": header_match.group(3),
                "summary": "",
                "keywords": ""
            }
        elif line.startswith("SUMMARY:"):
            if current_topic: current_topic["summary"] = line.replace("SUMMARY:", "").strip()
        elif line.startswith("KEYWORDS:"):
            if current_topic: current_topic["keywords"] = line.replace("KEYWORDS:", "").strip()
            
    if current_topic: topics.append(current_topic)
    return topics

def get_sentiment_label_for_segment(sentiment_data, start_sec, end_sec):
    """Returns Positive / Negative / Neutral for a topic segment"""
    if not sentiment_data:
        return "Neutral" 
    
    
    if isinstance(sentiment_data, list):
         df = pd.DataFrame(sentiment_data)
    else:
         return "Neutral"

    segment_df = df[(df["start"] >= start_sec) & (df["end"] <= end_sec)]
    
    if segment_df.empty:
        return "Neutral"
        
    avg_score = segment_df["score"].mean()
    if avg_score > 0.05: return "Positive"
    elif avg_score < -0.05: return "Negative"
    return "Neutral"

def run_tests():
    """Runs the unit tests and captures output."""
    if not TESTS_DIR.exists():
        return "Tests directory not found.", False

    # Add tests directory to path so we can import modules if needed
    if str(TESTS_DIR) not in sys.path:
        sys.path.append(str(TESTS_DIR))
        
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS_DIR))
    
    # Capture output
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    return stream.getvalue(), result.wasSuccessful()

# --- MAIN LOGIC ---
available_files = get_file_list(search_query)

# Handle case where no files are available
if not available_files:
    if search_query:
        st.warning(f"No podcasts found matching '{search_query}'.")
    else:
        st.info("👋 Welcome! Upload your first podcast to begin.")

selected_podcast = available_files[0] if available_files else None
if available_files and len(available_files) > 1:
     selected_podcast = st.selectbox("Select Episode", available_files, index=0)


# --- KEYWORD SENTIMENT INDICATOR ---
if search_query and selected_podcast:
    s_path = SENTIMENT_DIR / f"{selected_podcast}_sentiment.json"
    if s_path.exists():
        try:
            s_data = json.loads(s_path.read_text(encoding='utf-8'))
            
            # Find score of sentences containing the keyword
            scores = [s['score'] for s in s_data if search_query.lower() in s['text'].lower()]
            
            if scores:
                avg_score = sum(scores) / len(scores)
                
                if avg_score >= 0.05:
                    search_sentiment = ":green[Positive]"
                elif avg_score <= -0.05:
                    search_sentiment = ":red[Negative]"
                else:
                    search_sentiment = ":gray[Neutral]"
                    
                st.markdown(f"##### 🔎 Topic Sentiment for '{search_query}': **{search_sentiment}**")
        except:
            pass


tab_overview, tab_analysis, tab_transcript = st.tabs(["📌 Overview", "📊 Visualization", "📜 Transcript & Search"])


with tab_overview:
    if not selected_podcast:
        st.info("Please upload a podcast to view insights.")
    else:
        col_sum, col_key = st.columns([2, 1])
        
        with col_sum:
            st.markdown("### 📝 Smart Summary")
            summary_text = load_data(SUMMARY_DIR, f"{selected_podcast}_summary.txt")
            if not summary_text:
                transcript_json = load_data(TRANSCRIPT_DIR, f"{selected_podcast}.json", is_json=True)
                if transcript_json:
                    summary_text = transcript_json.get('text', '')[:500] + "..."
                    st.caption("⚠️ AI Summary pending. Showing transcript preview:")
            
            if summary_text:
                st.markdown(f'<div class="metric-card">{summary_text}</div>', unsafe_allow_html=True)
            else:
                st.info("No content available for summary.")
                
        with col_key:
            st.markdown("### 🔑 Top Keywords")
            keywords_text = load_data(KEYWORD_DIR, f"{selected_podcast}_keywords.txt")
            if keywords_text:
                kws = [line.strip() for line in keywords_text.splitlines() if not line.startswith("===")]
                for kw in kws[:10]: st.caption(f"🏷️ {kw}")
            else:
                st.info("Keywords pending...")

        st.divider()
        st.markdown("### 📚 Topic Segments & Analysis")
        
        topics_text = load_data(TOPIC_DIR, f"{selected_podcast}_topics.txt")
        sentiment_data = load_data(SENTIMENT_DIR, f"{selected_podcast}_sentiment.json", is_json=True)
        
        if topics_text:
            parsed_topics = parse_topics(topics_text)
            
            
            df_sent = pd.DataFrame(sentiment_data) if sentiment_data else pd.DataFrame()
            
            if parsed_topics:
                for i, t in enumerate(parsed_topics):
                  
                    sentiment_label = "Neutral"
                    sentiment_color = "gray"
                    
                    if not df_sent.empty:
                        mask = (df_sent['start'] >= t['start_sec']) & (df_sent['end'] <= t['end_sec'])
                        topic_scores = df_sent.loc[mask, 'score']
                        
                        if not topic_scores.empty:
                            avg = topic_scores.mean()
                            if avg >= 0.05:
                                sentiment_label = "Positive"
                                sentiment_color = "green"
                            elif avg <= -0.05:
                                sentiment_label = "Negative"
                                sentiment_color = "red"
                    
                   
                    with st.expander(
                        f"⏱️ {t['start_str']} - {t['end_str']} | {t['title']} "
                        f"| Sentiment: :{sentiment_color}[{sentiment_label}]"
                    ):
                        st.markdown(f"**Summary:** {t['summary']}")
                        st.caption(f"**Keywords:** {t['keywords']}")
            else:
                st.text_area("Detected Topics", topics_text, height=300)
        else:
            st.warning("Topic segmentation not available.")


with tab_analysis:
    if not selected_podcast:
        st.info("Please upload a podcast to view visualizations.")
    else:
        st.markdown("### 📈 Full Episode Emotional Journey")
        sentiment_data = load_data(SENTIMENT_DIR, f"{selected_podcast}_sentiment.json", is_json=True)

        if sentiment_data:
           
            df = pd.DataFrame(sentiment_data)
            df['Trend'] = df['score'].rolling(window=20, min_periods=1).mean()
            
            m1, m2, m3 = st.columns(3)
            avg_score = df['score'].mean()
            tone = "Positive" if avg_score > 0.05 else "Negative" if avg_score < -0.05 else "Neutral"
            m1.metric("Overall Tone", tone, delta=f"{avg_score:.2f}")
            m2.metric("Duration", f"{int(df['end'].max() // 60)} mins")
            m3.metric("Data Points", len(df))

            col_chart, col_pie = st.columns([3, 1])
            with col_chart:
                fig = px.bar(df, x="start", y="score", color="label",
                             color_discrete_map={'Positive': '#10B981', 'Negative': '#EF4444', 'Neutral': '#D1D5DB'},
                             labels={'start': 'Time (s)', 'score': 'Sentiment Intensity'},
                             title="Sentiment Flow vs. Trend Line", opacity=0.4)
                fig.add_scatter(x=df['start'], y=df['Trend'], mode='lines', name='Trend', line=dict(color='#4F46E5', width=3))
                fig.update_layout(plot_bgcolor='white', height=400)
                st.plotly_chart(fig, use_container_width=True)
                
            with col_pie:
                st.markdown("**Mood Distribution**")
                pie_fig = px.pie(df, names='label', color='label',
                                 color_discrete_map={'Positive': '#10B981', 'Negative': '#EF4444', 'Neutral': '#D1D5DB'},
                                 hole=0.4)
                pie_fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=250)
                st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.warning("Sentiment data not found.")


with tab_transcript:
    if not selected_podcast:
        st.info("Please upload a podcast to view the transcript.")
    else:
        st.markdown("### 📜 Full Transcript")
        highlight_term = st.text_input("Highlight keyword in text:", value=search_query if search_query else "")
        transcript_json = load_data(TRANSCRIPT_DIR, f"{selected_podcast}.json", is_json=True)
        
        if transcript_json:
            full_text = transcript_json.get('text', '')
            if highlight_term:
                pattern = re.compile(re.escape(highlight_term), re.IGNORECASE)
                highlighted_text = pattern.sub(lambda m: f'<span class="highlight">{m.group(0)}</span>', full_text)
                st.markdown(f'<div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; height: 500px; overflow-y: scroll; color: black;">{highlighted_text}</div>', unsafe_allow_html=True)
                count = len(re.findall(pattern, full_text))
                st.caption(f"Found {count} occurrences of '{highlight_term}'")
            else:
                st.text_area("Content", full_text, height=500)
        else:
            st.error("Transcript file missing.")
