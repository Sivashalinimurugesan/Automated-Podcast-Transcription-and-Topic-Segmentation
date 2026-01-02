from src.sentiment import analyze_segment_sentiment

def test_sentiment_output_structure():
    result = analyze_segment_sentiment("patient has severe pain")

    assert isinstance(result, dict)
    assert "label" in result
    assert "score" in result

def test_sentiment_score_range():
    result = analyze_segment_sentiment("normal blood pressure")
    assert 0.0 <= result["score"] <= 1.0
