import os
import nltk
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
from pydub import AudioSegment
from textblob import TextBlob  # Add this for Milestone 5

# Load Models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Milestone 5: Sentiment Analysis Function ---
def get_sentiment(text):
    """
    Analyzes the emotional tone of the segment.
    Returns: POSITIVE, NEGATIVE, or NEUTRAL.
    """
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    if score > 0.1:
        return "POSITIVE"
    elif score < -0.1:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

def format_time(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{int(m):02d}:{int(s):02d}"

def extract_keywords(segment):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([segment])
        scores = tfidf_matrix.toarray()[0]
        word_scores = list(zip(vectorizer.get_feature_names_out(), scores))
        sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
        # Professional clean keywords for UI
        return [w[0].upper() for w in sorted_words[:4]] 
    except:
        return []

def summarize_segment(segment):
    words = segment.split()
    if len(words) < 40:
        return segment
    try:
        max_len = min(70, len(words))
        min_len = min(30, max_len - 5)
        res = summarizer(segment, max_length=max_len, min_length=min_len, do_sample=False)
        return res[0]["summary_text"]
    except:
        return segment[:200]

def embedding_segmentation(text):
    sentences = nltk.sent_tokenize(text)
    if not sentences: return []
    embeddings = model.encode(sentences)
    similarities = []
    for i in range(1, len(embeddings)):
        sim = util.cos_sim(embeddings[i], embeddings[i-1]).item()
        similarities.append(sim)
    
    threshold = np.mean(similarities) - np.std(similarities) if similarities else 0
    segments = []
    current_segment = sentences[0]
    for i in range(1, len(sentences)):
        if similarities[i-1] < threshold:
            segments.append(current_segment)
            current_segment = sentences[i]
        else:
            current_segment += " " + sentences[i]
    segments.append(current_segment)
    return segments

# --- Main Export Function Updated for Analytics ---
def process_segments(text, wav_path):
    audio = AudioSegment.from_file(wav_path)
    total_sec = len(audio) / 1000 
    
    segments_text = embedding_segmentation(text)
    if not segments_text: return []
    
    seg_dur = total_sec // len(segments_text)
    final_output = []
    for i, seg in enumerate(segments_text):
        final_output.append({
            "segment_number": i + 1,
            "start_time": format_time(i * seg_dur),
            "end_time": format_time((i + 1) * seg_dur),
            "text": seg,
            "sentiment": get_sentiment(seg),        # Milestone 5: Added sentiment label
            "keywords": extract_keywords(seg),      # Milestone 3: Professional keywords
            "summary": summarize_segment(seg)       # Milestone 3: AI Summaries
        })
    return final_output