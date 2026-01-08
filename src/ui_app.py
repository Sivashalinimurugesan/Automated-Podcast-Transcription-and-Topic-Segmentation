import os
import streamlit as st
import pandas as pd
import plotly.express as px


# -------------------------------------------------
# App Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Automated Podcast / HR Interview Analysis",
    layout="wide"
)

st.title("🎙️ Automated Podcast / HR Interview Transcription & Topic Segmentation")
st.caption("End-to-end ASR, topic segmentation, summaries, and evaluation")


# -------------------------------------------------
# Paths
# -------------------------------------------------
AUDIO_DIR = "audio_processed"
TRANSCRIPT_DIR = "transcripts/final_asr"
SEGMENT_DIR = "segments"
EVAL_FILE = "docs/semantic_evaluation.csv"


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------
def load_text(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_segments(segment_file_path):
    segments = []
    current = None

    with open(segment_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("Segment"):
                if current:
                    segments.append(current)
                current = {
                    "title": line,
                    "keywords": "",
                    "summary": "",
                    "text": ""
                }

            elif line.startswith("Keywords:") and current:
                current["keywords"] = line.replace("Keywords:", "").strip()

            elif line.startswith("Summary:") and current:
                current["summary"] = line.replace("Summary:", "").strip()

            elif current and line:
                current["text"] += line + " "

        if current:
            segments.append(current)

    return segments


def load_evaluation_scores():
    scores = {}
    if not os.path.exists(EVAL_FILE):
        return scores

    df = pd.read_csv(EVAL_FILE)
    for _, row in df.iterrows():
        scores[row["session"]] = row["semantic_similarity"]
    return scores


# -------------------------------------------------
# Sidebar — Session Selection
# -------------------------------------------------
st.sidebar.header("📂 Available Sessions")

if not os.path.exists(TRANSCRIPT_DIR):
    st.error("Transcript directory not found.")
    st.stop()

sessions = sorted(
    f.replace(".txt", "")
    for f in os.listdir(TRANSCRIPT_DIR)
    if f.endswith(".txt")
)

selected_session = st.sidebar.selectbox(
    "Select Session",
    sessions
)

evaluation_scores = load_evaluation_scores()


# -------------------------------------------------
# Session Header
# -------------------------------------------------
st.subheader(f"Session: {selected_session}")

if selected_session in evaluation_scores:
    st.metric(
        "Semantic Similarity (ASR vs Manual)",
        f"{evaluation_scores[selected_session]:.2f}"
    )


# -------------------------------------------------
# Audio Playback
# -------------------------------------------------
audio_path = os.path.join(
    AUDIO_DIR, f"{selected_session}.Mix-Lapel.wav"
)

if os.path.exists(audio_path):
    st.subheader("🔊 Audio Playback")
    st.audio(audio_path)
else:
    st.warning("Audio file not found.")


# -------------------------------------------------
# Transcript View
# -------------------------------------------------
st.subheader("📄 Full Transcript")

transcript_path = os.path.join(
    TRANSCRIPT_DIR, f"{selected_session}.txt"
)

full_transcript = load_text(transcript_path)

st.text_area(
    "Transcript",
    full_transcript,
    height=250
)


# -------------------------------------------------
# Topic Segments
# -------------------------------------------------
st.subheader("🧩 Topic Segments")

segment_path = os.path.join(
    SEGMENT_DIR, f"{selected_session}_segments.txt"
)

if os.path.exists(segment_path):
    segments = load_segments(segment_path)

    sentiment_values = []

    for i, seg in enumerate(segments, start=1):
        sentiment_values.append(len(seg["text"].split()))

        with st.expander(f"Segment {i}"):
            st.markdown(f"**Keywords:** {seg['keywords']}")
            st.markdown(f"**Summary:** {seg['summary']}")
            st.write(seg["text"])

    # Simple visualization: segment length
    df_vis = pd.DataFrame({
        "Segment": [f"Segment {i}" for i in range(1, len(sentiment_values) + 1)],
        "Word Count": sentiment_values
    })

    fig = px.bar(
        df_vis,
        x="Segment",
        y="Word Count",
        title="Segment Length Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Segment file not found.")


# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Automated Podcast / HR Interview Transcription & Topic Segmentation "
    "| Springboard Internship Project"
)
