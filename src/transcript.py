import whisper
import re

model = whisper.load_model("base")

def summarize_text(text, max_sentences=4):
    if not text:
        return ""

    # Proper sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    summary_sentences = sentences[:max_sentences]
    summary = " ".join(summary_sentences).strip()

    # Ensure clean ending
    if summary and summary[-1] not in ".!?":
        summary += "."

    return summary


def transcribe_audio(audio_path):
    result = model.transcribe(audio_path, fp16=False)

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })

    full_text = " ".join(s["text"] for s in segments)

    return {
        "full_text": full_text,
        "summary": summarize_text(full_text),
        "segments": segments
    }
