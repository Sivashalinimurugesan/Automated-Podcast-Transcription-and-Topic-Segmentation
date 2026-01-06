import streamlit as st
import os, json, re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from config import AUDIO_PROCESSED_DIR, SEGMENTS_DIR

nltk.data.path.append(r"C:\Users\USER\nltk_data")

# ---------------- HELPERS ----------------
POS = {"improve","recovery","effective","benefit","stable"}
NEG = {"pain","risk","infection","failure","severe"}

def extract_sentiment_words(text):
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return {
        "Positive": [w for w in words if w in POS],
        "Negative": [w for w in words if w in NEG],
        "Neutral": [w for w in words if w not in POS and w not in NEG]
    }

# ---------------- UI STYLE ----------------
st.set_page_config("MEDI-LENS", layout="wide")
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg,#ff9a56,#ff6f91); }
.card {
 background:white;
 padding:16px;
 border-radius:14px;
 box-shadow:0 4px 12px rgba(0,0,0,.25);
 margin-bottom:12px;
}
.center { text-align:center; }
.big { font-size:56px; font-weight:800; }
.slogan { font-size:22px; opacity:0.9; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "started" not in st.session_state:
    st.session_state.started = False

# ================= LANDING PAGE =================
if not st.session_state.started:
    st.markdown("<div class='center big'>🩺 MEDI-LENS</div>", unsafe_allow_html=True)
    st.markdown("<div class='center slogan'>Medical Audio → Actionable Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='card'>🎧 Audio → Clean Medical Transcripts</div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'>📊 Keyword-based Sentiment Insight</div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'>☁ Smart Keyword Exploration</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([2,1,2])
    if mid.button("▶ START"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# ================= MAIN APP =================
tab1, tab2, tab3 = st.tabs([
    "🎧 Audio upload",
    "📊 Sentiment",
    "☁ Keyword Explorer"
])

# ---------------- AUDIO NAVIGATOR ----------------
with tab1:
    uploaded = st.file_uploader("Upload audio", type=["mp3","wav"])
    files = [f for f in os.listdir(AUDIO_PROCESSED_DIR) if f.endswith((".mp3",".wav"))]

    # Save uploaded file
    if uploaded:
        audio_path = os.path.join(AUDIO_PROCESSED_DIR, uploaded.name)
        open(audio_path,"wb").write(uploaded.read())
    elif files:
        audio_path = os.path.join(AUDIO_PROCESSED_DIR, st.selectbox("Select audio", files))
    else:
        st.info("Upload audio to begin")
        st.stop()

    st.audio(open(audio_path,"rb").read())

    # Find JSON matching the audio
    base = os.path.splitext(os.path.basename(audio_path))[0]
    default_json = os.path.join(SEGMENTS_DIR, f"{base}_segments.json")

    # List all JSONs in SEGMENTS_DIR
    json_files = [f for f in os.listdir(SEGMENTS_DIR) if f.endswith("_segments.json")]

    # Let user select JSON if default not found
    if os.path.exists(default_json):
        json_path = default_json
    elif json_files:
        selected_json = st.selectbox("Transcript JSON not found for this audio. Select one:", json_files)
        json_path = os.path.join(SEGMENTS_DIR, selected_json)
    else:
        st.error(f"No transcript JSONs found in {SEGMENTS_DIR}")
        st.stop()

    segments = json.load(open(json_path))

    c1, c2, c3 = st.columns(3)
    show_full = c1.button("📄 Full Transcription")
    show_seg = c2.button("🧩 Segments")
    clear = c3.button("🧹 Clear")

    search = st.text_input("🔍 Search keyword in transcript")

    if clear:
        st.rerun()

    if show_full:
        st.markdown("<div class='card'>" + " ".join(s["text"] for s in segments) + "</div>", unsafe_allow_html=True)

    if show_seg or search:
        for s in segments:
            if not search or search.lower() in s["text"].lower():
                st.markdown(
                    f"<div class='card'><b>Segment {s['segment_id']}</b><br>{s['text']}</div>",
                    unsafe_allow_html=True
                )

# ---------------- SENTIMENT ----------------
with tab2:
    pos, neg, neu = [], [], []

    for s in segments:
        sw = extract_sentiment_words(s["text"])
        pos += sw["Positive"]
        neg += sw["Negative"]
        neu += sw["Neutral"]

    counts = {"Positive":len(pos),"Neutral":len(neu),"Negative":len(neg)}

    col1, col2 = st.columns([1,3])
    with col1:
        fig, ax = plt.subplots(figsize=(2.2,1.6))
        ax.bar(counts.keys(), counts.values())
        ax.set_title("Sentiment Words", fontsize=9)
        ax.tick_params(labelsize=8)
        st.pyplot(fig)

    with col2:
        st.markdown("**Positive:** " + (", ".join(set(pos)) or "—"))
        st.markdown("**Negative:** " + (", ".join(set(neg)) or "—"))
        st.markdown("**Neutral:** " + (", ".join(list(set(neu))[:12]) or "—"))

# ---------------- KEYWORD CLOUD ----------------
with tab3:
    full_text = " ".join(s["text"] for s in segments).lower()
    words = re.findall(r"\b[a-z]{3,}\b", full_text)
    stop = set(TfidfVectorizer(stop_words="english").get_stop_words())
    words = [w for w in words if w not in stop]

    freq = dict(Counter(words).most_common(15))

    wc = WordCloud(
        width=300,
        height=180,
        background_color="white",
        colormap="plasma"
    ).generate_from_frequencies(freq)

    fig, ax = plt.subplots(figsize=(4,2.3))
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)

    kw = st.selectbox("Select keyword", list(freq.keys()))
    for s in segments:
        if kw in s["text"].lower():
            st.markdown(f"<div class='card'>{s['text']}</div>", unsafe_allow_html=True)
