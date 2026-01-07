# ================= INSTALL =================
# !pip install -q gradio openai-whisper keybert sentence-transformers nltk textblob matplotlib soundfile wordcloud

# ================= IMPORTS =================
import gradio as gr
import whisper
import tempfile
import soundfile as sf
import numpy as np
from keybert import KeyBERT
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt
import io, base64, nltk, re, os
from nltk.tokenize import sent_tokenize
from wordcloud import WordCloud

nltk.download("punkt")

# ================= MODELS =================
stt_model = whisper.load_model("small")
kw_model = KeyBERT()

# ================= GLOBAL STATE =================
SEGMENTS = []
TRANSCRIPT = ""
KEYWORDS = []

# ================= SENTIMENT RANGE =================
def sentiment_range(score):
    if score > 0.3:
        return "🟢 Strong Positive"
    elif score > 0.1:
        return "🟢 Mild Positive"
    elif score >= -0.1:
        return "🟡 Neutral"
    elif score >= -0.3:
        return "🔴 Mild Negative"
    else:
        return "🔴 Strong Negative"

# ================= HIGHLIGHT =================
def highlight(text, keyword):
    return re.sub(
        fr"({keyword})",
        r"<span style='background:#ffd54f;color:black;padding:2px 6px;border-radius:4px;font-weight:bold'>\1</span>",
        text,
        flags=re.IGNORECASE
    )

# ================= SUMMARY =================
def smart_summary(sentences):
    if len(sentences) <= 6:
        return " ".join(sentences)
    return " ".join(sentences[:3] + sentences[len(sentences)//2:len(sentences)//2+2] + sentences[-2:])

# ================= AUDIO SAFE LOADER =================
def load_audio(audio):
    # gradio.live returns filepath
    if isinstance(audio, str):
        return audio

    # local numpy audio
    sr, data = audio
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, data, sr)
    return tmp.name

# ================= MAIN PIPELINE =================
def analyze_audio(audio):
    global SEGMENTS, TRANSCRIPT, KEYWORDS

    if audio is None:
        return "❌ Please upload audio", "", "", "", "", gr.update(choices=[]), ""

    audio_path = load_audio(audio)

    result = stt_model.transcribe(audio_path, fp16=False)
    TRANSCRIPT = result["text"]

    sentences = sent_tokenize(TRANSCRIPT)
    summary = smart_summary(sentences)

    # -------- SEGMENTS --------
    SEGMENTS = []
    seg_len = max(1, len(sentences) // 8)

    i = sid = 0
    while i < len(sentences):
        text = " ".join(sentences[i:i+seg_len])
        score = TextBlob(text).sentiment.polarity
        SEGMENTS.append({
            "id": sid,
            "text": text,
            "score": score,
            "range": sentiment_range(score)
        })
        i += seg_len
        sid += 1

    # -------- KEYWORDS --------
    KEYWORDS = [k for k, _ in kw_model.extract_keywords(
        TRANSCRIPT,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=20
    )]

    return (
        summary,
        TRANSCRIPT,
        keyword_visuals(),
        sentiment_timeline(),
        keyword_insights(),
        gr.update(choices=KEYWORDS),
        build_all_segments()
    )

# ================= KEYWORD VISUALS =================
def keyword_visuals():
    freq = Counter()
    for kw in KEYWORDS:
        for s in SEGMENTS:
            freq[kw] += s["text"].lower().count(kw.lower())

    if not freq:
        return "No keywords"

    fig, ax = plt.subplots(figsize=(7, 4))
    words, counts = zip(*freq.most_common(10))
    ax.barh(words[::-1], counts[::-1])
    ax.set_title("Top Keywords")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)

    return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}'>"

# ================= INSIGHTS =================
def keyword_insights():
    pos = sum(1 for s in SEGMENTS if s["score"] > 0.1)
    neg = sum(1 for s in SEGMENTS if s["score"] < -0.1)
    neu = len(SEGMENTS) - pos - neg

    return f"""
### 🌟 Insights
- 🟢 Positive: **{pos}**
- 🟡 Neutral: **{neu}**
- 🔴 Negative: **{neg}**
- 🔑 Keywords: **{len(KEYWORDS)}**
"""

# ================= SENTIMENT TIMELINE =================
def sentiment_timeline():
    scores = [s["score"] for s in SEGMENTS]

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(scores, marker="o")
    ax.axhline(0, linestyle="--")
    ax.set_ylim(-1, 1)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)

    return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}'>"

# ================= SEGMENTS =================
def build_all_segments():
    return "\n\n".join(
        f"### Segment {s['id']+1}\n{s['range']}\n\n{s['text']}"
        for s in SEGMENTS
    )

# ================= KEYWORD SEARCH =================
def keyword_jump(keyword):
    return "\n\n".join(
        highlight(s["text"], keyword)
        for s in SEGMENTS if keyword.lower() in s["text"].lower()
    ) or "No segments found"

# ================= UI =================
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎧 Medical Podcast Intelligence Platform")

    audio = gr.Audio(type="numpy", label="Upload Podcast Audio")
    btn = gr.Button("🚀 Analyze")

    with gr.Tab("🧠 Summary"):
        summary = gr.Markdown()

    with gr.Tab("📝 Transcript"):
        transcript = gr.Textbox(lines=12)

    with gr.Tab("📊 Keyword Analytics"):
        keyword_stats = gr.HTML()
        insights = gr.Markdown()

    with gr.Tab("📈 Sentiment"):
        timeline = gr.HTML()

    with gr.Tab("🔑 Keyword Search"):
        keyword_dd = gr.Dropdown()
        keyword_segments = gr.Markdown()

    with gr.Tab("📍 All Segments"):
        all_segments = gr.Markdown()

    btn.click(
        analyze_audio,
        audio,
        [summary, transcript, keyword_stats, timeline, insights, keyword_dd, all_segments]
    )

    keyword_dd.change(keyword_jump, keyword_dd, keyword_segments)

app.launch(share=True)
