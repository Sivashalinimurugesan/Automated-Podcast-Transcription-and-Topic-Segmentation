import streamlit as st
import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# -----------------------
# PATH CONFIGURATION
# -----------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
SEGMENTED_DIR = os.path.join(BASE_DIR, "segmented")
KEYWORDS_DIR = os.path.join(BASE_DIR, "keywords")
AUDIO_DIR = os.path.join(BASE_DIR, "audio_processed")

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Automated Podcast Dashboard",
    layout="wide"
)

st.markdown("## 🎧 Automated Podcast Transcription & Topic Segmentation Dashboard")

# -----------------------
# HELPER FUNCTIONS
# -----------------------

def list_files(folder, extensions=None):
    if not os.path.exists(folder):
        return []
    files = os.listdir(folder)
    if extensions:
        files = [f for f in files if f.lower().endswith(extensions)]
    return sorted(files)


def read_text_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


def plot_top_words(text, top_n=10):
    words = text.lower().split()
    counter = Counter(words)
    common = counter.most_common(top_n)

    if not common:
        st.warning("No data available for visualization.")
        return

    labels = [x[0] for x in common]
    values = [x[1] for x in common]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_title("Top Words Frequency")
    ax.set_ylabel("Count")
    ax.set_xlabel("Words")
    plt.xticks(rotation=30)

    st.pyplot(fig)


def generate_wordcloud(text):
    if not text.strip():
        st.warning("No text available for WordCloud.")
        return

    wc = WordCloud(
        width=900,
        height=400,
        background_color="white"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)


# -----------------------
# TABS
# -----------------------

tabs = st.tabs([
    "⬆ Upload",
    "📄 Transcript",
    "✂ Topic Segments",
    "🔑 Keywords",
    "📈 Visualizations",
    "🎧 Cleaned Audio"
])

# -----------------------
# TAB 1 — UPLOAD
# -----------------------
with tabs[0]:
    st.subheader("Upload Transcript File")

    uploaded_file = st.file_uploader(
        "Upload a text file",
        type=["txt"]
    )

    if uploaded_file:
        save_path = os.path.join(TRANSCRIPTS_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File uploaded successfully: {uploaded_file.name}")


# -----------------------
# TAB 2 — TRANSCRIPT
# -----------------------
with tabs[1]:
    st.subheader("Transcript Viewer")

    transcript_files = list_files(TRANSCRIPTS_DIR, (".txt",))

    if transcript_files:
        selected_file = st.selectbox("Select transcript file", transcript_files)
        text = read_text_file(os.path.join(TRANSCRIPTS_DIR, selected_file))
        st.text_area("Transcript", text, height=300)
    else:
        st.warning("No transcript files found.")


# -----------------------
# TAB 3 — SEGMENTS
# -----------------------
with tabs[2]:
    st.subheader("Topic Segments")

    segment_files = list_files(SEGMENTED_DIR, (".txt",))

    if segment_files:
        selected_segment = st.selectbox("Select segment file", segment_files)
        seg_text = read_text_file(os.path.join(SEGMENTED_DIR, selected_segment))
        st.text_area("Segmented Text", seg_text, height=300)
    else:
        st.warning("No segmented files found.")


# -----------------------
# TAB 4 — KEYWORDS
# -----------------------
with tabs[3]:
    st.subheader("Extracted Keywords")

    keyword_files = list_files(KEYWORDS_DIR, (".txt",))

    if keyword_files:
        selected_key = st.selectbox("Select keyword file", keyword_files)
        key_text = read_text_file(os.path.join(KEYWORDS_DIR, selected_key))
        st.text_area("Keywords", key_text, height=200)
    else:
        st.warning("No keyword files found.")


# -----------------------
# TAB 5 — VISUALIZATION
# -----------------------
with tabs[4]:
    st.subheader("Text Visualizations")

    transcript_files = list_files(TRANSCRIPTS_DIR, (".txt",))

    if transcript_files:
        selected_vis_file = st.selectbox("Select transcript for visualization", transcript_files)
        vis_text = read_text_file(os.path.join(TRANSCRIPTS_DIR, selected_vis_file))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Top Words Frequency")
            plot_top_words(vis_text)

        with col2:
            st.markdown("### ☁ Word Cloud")
            generate_wordcloud(vis_text)

    else:
        st.warning("No transcript files available for visualization.")


# -----------------------
# TAB 6 — CLEANED AUDIO
# -----------------------
with tabs[5]:
    st.subheader("Cleaned Audio Files")

    audio_files = list_files(AUDIO_DIR, (".wav", ".mp3"))

    if audio_files:
        selected_audio = st.selectbox("Select cleaned audio", audio_files)
        audio_path = os.path.join(AUDIO_DIR, selected_audio)

        st.audio(audio_path)
        st.success(f"Playing: {selected_audio}")

    else:
        st.warning("No cleaned audio files found in audio_processed folder.")


# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("🎧 Automated Podcast Transcription & Topic Segmentation | Streamlit NLP Dashboard")
