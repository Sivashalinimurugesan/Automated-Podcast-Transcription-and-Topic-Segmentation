import re
from collections import Counter

# -------------------------------------------------
# Sentence segmentation
# -------------------------------------------------
def sentence_based_segments(text):
    if not text.strip():
        return []

    parts = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    segments = []

    for i, p in enumerate(parts):
        p = p.strip()
        if len(p) > 2:
            segments.append({
                "segment_id": i + 1,
                "text": p
            })

    return segments


# -------------------------------------------------
# Text summarization
# -------------------------------------------------
def summarize_text(text, top_n=8):
    if not text.strip():
        return ""

    sentences = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    freq = Counter(words)

    ranked = []
    for s in sentences:
        score = sum(freq.get(w.lower(), 0) for w in re.findall(r'\b[a-zA-Z]+\b', s))
        ranked.append((score, s))

    ranked = sorted(ranked, reverse=True)
    summary = " ".join([s for _, s in ranked[:top_n]])

    return summary


# -------------------------------------------------
# Speaker detection
# -------------------------------------------------
def detect_speaker(text):
    t = text.lower()

    narrator_markers = ["welcome", "today we", "before you go", "remember", "thank you for watching"]
    interviewer_patterns = ["what is", "why do you", "how long", "how did you", "can you", "do you", "tell me"]
    candidate_patterns = ["i am", "i'm", "i studied", "i work", "i have been", "my experience", "i want"]

    if any(p in t for p in narrator_markers):
        return "Narrator"
    if t.strip().endswith("?") or any(p in t for p in interviewer_patterns):
        return "Interviewer"
    if any(p in t for p in candidate_patterns):
        return "Candidate"
    return "Narrator"
