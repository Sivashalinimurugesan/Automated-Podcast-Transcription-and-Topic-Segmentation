from backend.audio_preprocessing.preprocess import analyze_sentiment

def test_sentiment_empty_text():
    result = analyze_sentiment("")
    assert result == "neutral"
