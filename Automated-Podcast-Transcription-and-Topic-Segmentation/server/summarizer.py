import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
from textblob import TextBlob  # <--- NEW IMPORT
import config

def generate_summary(text, count=2):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    freq = {}
    for w in words:
        w = w.lower()
        if w.isalnum() and w not in stop_words:
            freq[w] = freq.get(w, 0) + 1
            
    sentences = sent_tokenize(text)
    ranking = {}
    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] = ranking.get(i, 0) + freq[w]
                
    top_indices = nlargest(count, ranking, key=ranking.get)
    return ' '.join([sentences[i] for i in sorted(top_indices)])

def get_keywords(text, num=5):
    stop_words = set(stopwords.words('english'))
    words = [w.lower() for w in word_tokenize(text) if w.isalnum() and w.lower() not in stop_words]
    return [w for w, c in nltk.FreqDist(words).most_common(num)]

# --- NEW FUNCTION: SENTIMENT ANALYSIS ---
def get_sentiment(text):
    analysis = TextBlob(text)
    # Returns a score between -1.0 (Negative) and 1.0 (Positive)
    return analysis.sentiment.polarity

def process_summaries():
    print("[SUMMARIZER] Generating final JSON with Sentiment...")
    files = [f for f in os.listdir(config.PROCESSED_FOLDER) if f.startswith("segments_")]
    final_results = []

    for filename in files:
        with open(os.path.join(config.PROCESSED_FOLDER, filename), "r", encoding="utf-8") as f:
            content = f.read()
            
        topics = content.split("=== TOPIC")
        for t in topics:
            if not t.strip(): continue
            
            lines = t.strip().split("\n", 1)
            topic_id = lines[0].strip()
            body = lines[1] if len(lines) > 1 else ""
            
            if len(body) < 10: continue

            final_results.append({
                "topic_id": topic_id,
                "summary": generate_summary(body),
                "keywords": get_keywords(body),
                "sentiment": get_sentiment(body), # <--- ADDED SENTIMENT HERE
                "text_snippet": body[:150] + "..."
            })
            
    return final_results