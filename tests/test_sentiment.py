# tests/test_sentiment.py
from src.preprocessing import analyze_sentiment  # function jahan ho, uske hisaab se path adjust karo

def test_sentiment_basic():
    text = "I love this podcast!"
    result = analyze_sentiment(text)
    # function 'positive', 'negative', 'neutral' return karega
    assert result in ["positive", "negative", "neutral"]

def test_sentiment_empty():
    text = ""
    result = analyze_sentiment(text)
    assert result == "neutral"
