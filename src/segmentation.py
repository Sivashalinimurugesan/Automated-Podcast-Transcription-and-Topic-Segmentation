import os
import json
import re
from transformers import pipeline
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from src.logger import get_logger

# -------------------------------------------------
# LOGGER
# -------------------------------------------------
logger = get_logger("SEGMENTATION", "pipeline.log")

# -------------------------------------------------
# MODELS
# -------------------------------------------------
summarizer = pipeline(
    "summarization",
    model="facebook/bart-base",
    device=-1
)

kw_model = KeyBERT(
    model=SentenceTransformer("all-MiniLM-L6-v2")
)

sentiment_model = pipeline("sentiment-analysis")

# -------------------------------------------------
# REGEX
# -------------------------------------------------
timestamp_pattern = re.compile(
    r"\[(\d{2}:\d{2}\.\d{2})\s*-\s*(\d{2}:\d{2}\.\d{2})\]\s*(.*)"
)

# -------------------------------------------------
# PARSE TRANSCRIPT
# -------------------------------------------------
def parse_transcript(text):
    parsed = []
    prev = None

    for line in text.splitlines():
        match = timestamp_pattern.match(line)
        if not match:
            continue

        start, end, sentence = match.groups()
        sentence = sentence.strip()

        if prev and sentence and sentence[0].islower():
            prev["text"] += " " + sentence
            prev["end"] = end
        else:
            prev = {"start": start, "end": end, "text": sentence}
            parsed.append(prev)

    return parsed

# -------------------------------------------------
# SEGMENT SENTENCES
# -------------------------------------------------
def segment_sentences(sentences, max_words=120):
    segments, current_text = [], []
    start_time = None

    for s in sentences:
        if start_time is None:
            start_time = s["start"]

        combined = " ".join(current_text + [s["text"]])
        if len(combined.split()) <= max_words:
            current_text.append(s["text"])
            end_time = s["end"]
        else:
            segments.append({
                "start_time": start_time,
                "end_time": end_time,
                "text": " ".join(current_text)
            })
            current_text = [s["text"]]
            start_time, end_time = s["start"], s["end"]

    if current_text:
        segments.append({
            "start_time": start_time,
            "end_time": end_time,
            "text": " ".join(current_text)
        })

    return segments

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def summarise(text):
    result = summarizer(
        text[:800],
        max_length=40,
        min_length=20,
        do_sample=False
    )
    return result[0]["summary_text"]

def extract_keywords(text):
    raw = kw_model.extract_keywords(text, top_n=8)
    return list({k[0] for k in raw})

def extract_sentiment(text):
    try:
        res = sentiment_model(text[:512])[0]
        return {"label": res["label"], "score": round(res["score"], 3)}
    except Exception:
        return {"label": "UNKNOWN", "score": 0.0}

# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------
def generate_segmentation(raw_text):
    parsed = parse_transcript(raw_text)
    segments = segment_sentences(parsed)

    output = {"segments": []}

    for idx, seg in enumerate(segments, 1):
        summary = summarise(seg["text"])
        output["segments"].append({
            "segment_id": idx,
            "segment_label": summary[:45],
            "segment_summary": summary,
            "start_time": seg["start_time"],
            "end_time": seg["end_time"],
            "segment_text": seg["text"],
            "keywords": extract_keywords(seg["text"]),
            "sentiment": extract_sentiment(seg["text"])
        })

    return output

# -------------------------------------------------
# 🔹 REQUIRED FOR FLASK
# -------------------------------------------------
def generate_segmentation_for_ui(transcript_text):
    return generate_segmentation(transcript_text)

# -------------------------------------------------
# BATCH MODE
# -------------------------------------------------
def main():
    transcripts_dir = "transcripts"
    output_dir = "segments"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(transcripts_dir):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(transcripts_dir, file), "r", encoding="utf-8") as f:
            raw_text = f.read()

        result = generate_segmentation(raw_text)

        with open(
            os.path.join(output_dir, file.replace(".txt", ".json")),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(result, f, indent=4)

        logger.info(f"Processed {file}")

if __name__ == "__main__":
    main()
