import os
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Automated Podcast Transcription",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRANSCRIPT_DIR = os.path.join(BASE_DIR, "..", "transcripts")
SEGMENTED_DIR = os.path.join(BASE_DIR, "..", "segmented")
KEYWORDS_DIR = os.path.join(BASE_DIR, "..", "keywords")
AUDIO_DIR = os.path.join(BASE_DIR, "..", "audio_processed")

# ---------------- SAFE FILE FINDER ----------------
def find_file(folder, base_name, must_contain):
    if not os.path.exists(folder):
        return None

    for f in os.listdir(folder):
        fname = f.lower()
        if base_name.lower() in fname and must_contain in fname:
            return os.path.join(folder, f)
    return None

# ---------------- HEADER ----------------
st.title("🎧 Automated Podcast Transcription & Topic Segmentation")
st.caption("AI-powered transcription, segmentation & keyword extraction")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📂 Select Transcript")

if not os.path.exists(TRANSCRIPT_DIR):
    st.sidebar.error("❌ transcripts folder not found")
    st.stop()

transcripts = sorted([f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".txt")])

if not transcripts:
    st.sidebar.warning("⚠️ No transcript files found")
    st.stop()

selected_file = st.sidebar.selectbox("Choose a transcript", transcripts)
base_name = os.path.splitext(selected_file)[0]

# ---------------- PATH RESOLUTION ----------------
transcript_path = os.path.join(TRANSCRIPT_DIR, selected_file)
segmented_path = find_file(SEGMENTED_DIR, base_name, "seg")
keywords_path = find_file(KEYWORDS_DIR, base_name, "key")
audio_path = find_file(AUDIO_DIR, base_name, "clean")

# ---------------- TRANSCRIPTION ----------------
st.header("📄 Transcription")

with open(transcript_path, "r", encoding="utf-8") as f:
    transcript_text = f.read()

st.text_area("Predicted Transcript", transcript_text, height=300)

# ---------------- CLEANED AUDIO ----------------
st.header("🎵 Cleaned Audio")

if audio_path:
    st.audio(audio_path)
else:
    st.warning("Cleaned audio not found")

# ---------------- SEGMENTED TEXT (PARAGRAPH MODE) ----------------
st.header("✂️ Segmented Text")

if segmented_path:
    with open(segmented_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    paragraph = " ".join(lines)
    st.write(paragraph)
else:
    st.warning("Segmented text not found")

# ---------------- KEYWORDS ----------------
st.header("🔑 Extracted Keywords")

if keywords_path:
    with open(keywords_path, "r", encoding="utf-8") as f:
        keywords = [k.strip() for k in f.read().replace("\n", ",").split(",") if k.strip()]
    st.write(", ".join(keywords))
else:
    st.warning("Keywords file not found")

# ---------------- KEYWORD SEARCH ----------------
st.header("🔍 Keyword Search")

query = st.text_input("Enter keyword to search")

if query:
    matches = [
        s.strip()
        for s in transcript_text.split(".")
        if query.lower() in s.lower()
    ]

    if matches:
        st.success(f"Found {len(matches)} matches")
        for m in matches:
            st.write("•", m)
    else:
        st.info("No matches found")
