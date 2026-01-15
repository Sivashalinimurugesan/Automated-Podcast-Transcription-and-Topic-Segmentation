from src.app_logic import compute_sentiment_label, aggregate_keyword_counts

def test_sentiment_positive():
    assert compute_sentiment_label("I love this product") == "positive"

def test_sentiment_negative():
    assert compute_sentiment_label("This is terrible") == "negative"

def test_sentiment_neutral():
    assert compute_sentiment_label("This is a chair") == "neutral"

def test_aggregate_keyword_counts():
    segments = [
        {"keywords": ["ai", "ml"]},
        {"keywords": ["ai"]},
        {"keywords": ["ml"]}
    ]

    counts = aggregate_keyword_counts(segments)

    assert counts["ai"] == 2
    assert counts["ml"] == 2
