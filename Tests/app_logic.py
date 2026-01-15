from textblob import TextBlob

def compute_sentiment_label(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"

def aggregate_keyword_counts(segments):
    keyword_counts = {}
    for seg in segments:
        for kw in seg.get("keywords", []):
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
    return keyword_counts
