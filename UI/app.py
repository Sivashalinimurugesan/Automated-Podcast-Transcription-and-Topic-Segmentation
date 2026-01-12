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
import io, base64, nltk, re
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
    if score > 0.3: return "🟢 Strong Positive"
    elif score > 0.1: return "🟢 Mild Positive"
    elif score >= -0.1: return "🟡 Neutral"
    elif score >= -0.3: return "🔴 Mild Negative"
    else: return "🔴 Strong Negative"

# ================= HIGHLIGHT =================
def highlight(text, keyword):
    return re.sub(
        fr"({keyword})",
        r"<span style='background:#ffcc80;padding:3px 6px;border-radius:6px;font-weight:bold'>\1</span>",
        text,
        flags=re.IGNORECASE
    )

# ================= PARAGRAPH SUMMARY (5–6 LINES) =================
def smart_summary(sentences):
    if len(sentences) <= 6:
        return " ".join(sentences)

    intro = sentences[:2]
    middle = sentences[len(sentences)//3 : len(sentences)//3 + 2]
    end = sentences[-2:]

    summary_sentences = intro + middle + end
    return " ".join(summary_sentences)

# ================= AUDIO LOADER =================
def load_audio(audio):
    if isinstance(audio, str):
        return audio
    sr, data = audio
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, data, sr)
    return tmp.name

# ================= MAIN PIPELINE =================
def analyze_audio(audio):
    global SEGMENTS, TRANSCRIPT, KEYWORDS

    audio_path = load_audio(audio)
    result = stt_model.transcribe(audio_path, fp16=False)
    TRANSCRIPT = result["text"]

    sentences = sent_tokenize(TRANSCRIPT)
    summary = smart_summary(sentences)

    SEGMENTS = []
    seg_len = max(1, len(sentences) // 8)

    i = sid = 0
    while i < len(sentences):
        text = " ".join(sentences[i:i+seg_len])
        score = TextBlob(text).sentiment.polarity
        SEGMENTS.append({
            "id": sid,
            "text": text,
            "score": round(score, 3),
            "range": sentiment_range(score)
        })
        i += seg_len
        sid += 1

    KEYWORDS = [k for k, _ in kw_model.extract_keywords(
        TRANSCRIPT,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=25
    )]

    return (
        summary,
        TRANSCRIPT,
        keyword_bar_graph(),
        keyword_wordcloud(),
        sentiment_timeline(),
        keyword_insights(),
        gr.update(choices=KEYWORDS),
        build_all_segments()
    )

# ================= KEYWORD BAR GRAPH =================
def keyword_bar_graph():
    freq = Counter()
    for kw in KEYWORDS:
        for s in SEGMENTS:
            freq[kw] += s["text"].lower().count(kw.lower())

    fig, ax = plt.subplots(figsize=(8, 4))
    words, counts = zip(*freq.most_common(10))
    ax.barh(words[::-1], counts[::-1])
    ax.set_title("Keyword Frequency Distribution")
    ax.grid(axis="x", alpha=0.3)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)

    return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}'>"

# ================= WORD CLOUD =================
def keyword_wordcloud():
    wc = WordCloud(
        width=900,
        height=400,
        background_color="white",
        colormap="viridis"
    ).generate(" ".join(KEYWORDS))

    buf = io.BytesIO()
    plt.figure(figsize=(9, 4))
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()

    return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}'>"

# ================= INSIGHTS =================
def keyword_insights():
    pos = sum(1 for s in SEGMENTS if s["score"] > 0.1)
    neg = sum(1 for s in SEGMENTS if s["score"] < -0.1)
    neu = len(SEGMENTS) - pos - neg

    return f"""
### 🔍 Overall Insights
- 🟢 Positive Segments: **{pos}**
- 🟡 Neutral Segments: **{neu}**
- 🔴 Negative Segments: **{neg}**
- 🔑 Keywords Extracted: **{len(KEYWORDS)}**
"""

# ================= SENTIMENT TIMELINE =================
def sentiment_timeline():
    scores = [s["score"] for s in SEGMENTS]
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(scores, marker="o")
    ax.axhline(0, linestyle="--")
    ax.set_ylim(-1, 1)
    ax.set_title("Sentiment Flow Across Podcast")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)

    return f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}'>"

# ================= SEGMENTS =================
def build_all_segments():
    return "\n\n".join(
        f"### Segment {s['id']+1}\n{s['range']} (Score: {s['score']})\n\n{s['text']}"
        for s in SEGMENTS
    )

# ================= KEYWORD SEARCH =================
def keyword_jump(keyword):
    matches = []
    for s in SEGMENTS:
        if keyword.lower() in s["text"].lower():
            matches.append(
                f"""
### 🔹 Segment {s['id']+1}
**Sentiment:** {s['range']}  
**Score:** `{s['score']}`  

{highlight(s['text'], keyword)}
"""
            )
    return "\n\n".join(matches) if matches else "❌ No segments found for this keyword."

# ================= UI =================
with gr.Blocks(theme=gr.themes.Soft(primary_hue="cyan")) as app:
    gr.Markdown("# 🏥 Medical Podcast Intelligence Platform")

    audio = gr.Audio(type="numpy", label="Upload Audio")
    btn = gr.Button("🚀 Analyze Podcast")

    with gr.Tab("🧠 Summary"):
        summary = gr.Markdown()
        transcript = gr.Textbox(lines=10, label="Full Transcript")

    with gr.Tab("📊 Keyword Analytics"):
        bar_graph = gr.HTML()
        wordcloud = gr.HTML()

    with gr.Tab("📈 Sentiment Analysis"):
        timeline = gr.HTML()
        insights = gr.Markdown()

    with gr.Tab("🔑 Keyword Explorer"):
        keyword_dd = gr.Dropdown(label="Select Keyword")
        keyword_segments = gr.Markdown()

    with gr.Tab("📍 All Segments"):
        all_segments = gr.Markdown()

    btn.click(
        analyze_audio,
        audio,
        [summary, transcript, bar_graph, wordcloud, timeline, insights, keyword_dd, all_segments]
    )

    keyword_dd.change(keyword_jump, keyword_dd, keyword_segments)

app.launch(share=True)
