import os
import json
from flask import (
    Flask, render_template, request,
    redirect, url_for, send_from_directory
)
from nltk.sentiment import SentimentIntensityAnalyzer

from preprocessing import clean_audio
from transcription import safe_transcribe_file
from summaries import process_file

# ======================
# APP CONFIG
# ======================
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "meettext-secret"

sia = SentimentIntensityAnalyzer()

# ======================
# PATHS
# ======================
AUDIO_SAMPLE_DIR = r"C:\Users\Dell\Desktop\meeting_workspace\Data_denver\Audio_sample"
CLEAN_WAV_DIR = r"C:\Users\Dell\Desktop\meeting_workspace\Data_denver\clean_wav"
TRANSCRIPT_DIR = r"C:\Users\Dell\Desktop\meeting_workspace\transcripts"
SUMMARY_DIR = r"C:\Users\Dell\Desktop\meeting_workspace\summaries"

# ======================
# HELPERS
# ======================
def list_existing_audio():
    if not os.path.exists(CLEAN_WAV_DIR):
        return []
    return [f for f in os.listdir(CLEAN_WAV_DIR) if f.endswith(".wav")]


def load_transcript(audio):
    path = os.path.join(
        TRANSCRIPT_DIR,
        audio.replace(".wav", "_transcription.txt")
    )
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_summary(audio):
    path = os.path.join(
        SUMMARY_DIR,
        audio.replace(".wav", ".json")
    )
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        # ------------------
        # EXISTING AUDIO
        # ------------------
        if request.form.get("mode") == "existing":
            audio = request.form.get("existing_file")
            if audio:
                return redirect(url_for("player", audio=audio))
            return redirect("/upload")

        # ------------------
        # NEW AUDIO
        # ------------------
        file = request.files.get("audio")
        if not file or file.filename == "":
            return redirect("/upload")

        raw_path = os.path.join(AUDIO_SAMPLE_DIR, file.filename)
        file.save(raw_path)

        wav_name = file.filename.replace(".mp3", ".wav")
        wav_path = os.path.join(CLEAN_WAV_DIR, wav_name)

        # Clean audio only once
        if not os.path.exists(wav_path):
            clean_audio(raw_path, wav_path)

        # Transcribe & summarize only once
        transcript_path = safe_transcribe_file(wav_path)
        process_file(transcript_path)

        # 👉 Redirect to PLAYER
        return redirect(url_for("player", audio=wav_name))

    return render_template(
        "upload.html",
        files=list_existing_audio()
    )


@app.route("/player/<audio>")
def player(audio):
    transcript = load_transcript(audio)
    summary = load_summary(audio)

    # ------------------
    # SAFETY NORMALIZATION
    # ------------------
    summary.setdefault("segments", [])
    summary.setdefault("top_keywords", [])
    summary.setdefault("sentiments", {})

    # Compatibility
    if "final_summary" not in summary and "summary" in summary:
        summary["final_summary"] = summary["summary"]

    # ------------------
    # BUILD KEYWORDS + SENTIMENTS
    # ------------------
    top_keywords = []
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}

    for seg in summary["segments"]:
        text = seg.get("text", "")

        # Sentiment
        score = sia.polarity_scores(text)["compound"]
        sentiment = (
            "positive" if score >= 0.05 else
            "negative" if score <= -0.05 else
            "neutral"
        )
        sentiments[sentiment] += 1
        seg["sentiment"] = sentiment

        # Timestamp safety
        seg.setdefault("timestamp", "00:00")

        # Keywords safety
        seg.setdefault("keywords", [])

        for kw in seg["keywords"]:
            if kw not in top_keywords:
                top_keywords.append(kw)

    # Limit keyword cloud size
    summary["top_keywords"] = top_keywords[:20]
    summary["sentiments"] = sentiments

    return render_template(
        "player.html",
        audio=audio,
        transcript=transcript,
        summary=summary,
        keywords=summary["top_keywords"]  # 🔑 EXPLICIT
    )


@app.route("/analytics")
def analytics():
    files = [
        f.replace(".json", ".wav")
        for f in os.listdir(SUMMARY_DIR)
        if f.endswith(".json")
    ]

    selected_audio = request.args.get("audio")
    if not selected_audio and files:
        selected_audio = files[0]

    data = load_summary(selected_audio)

    keywords = {}
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}

    for seg in data.get("segments", []):
        for kw in seg.get("keywords", []):
            keywords[kw] = keywords.get(kw, 0) + 1

        score = sia.polarity_scores(seg.get("text", ""))["compound"]
        sentiments[
            "positive" if score >= 0.05 else
            "negative" if score <= -0.05 else
            "neutral"
        ] += 1

    return render_template(
        "analytics.html",
        keywords=keywords,
        sentiments=sentiments,
        files=files,
        selected_audio=selected_audio
    )


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(CLEAN_WAV_DIR, filename)


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
