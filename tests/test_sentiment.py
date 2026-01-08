import sys
from collections import Counter
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import medical_sentiment, sentiment_distribution

def test_medical_sentiment_pos():
    txt = "Patient shows improvement and recovery"
    assert medical_sentiment(txt) == "Positive"

def test_medical_sentiment_neg():
    txt = "Patient has severe pain and infection"
    assert medical_sentiment(txt) == "Negative"

def test_medical_sentiment_neutral():
    txt = "Patient visited hospital for routine checkup"
    assert medical_sentiment(txt) == "Neutral"

def test_sentiment_distribution_basic():
    segments = [
        {"text": "Patient shows improvement"},
        {"text": "Patient has infection"},
        {"text": "Routine checkup"}
    ]
    dist = sentiment_distribution(segments)
    assert isinstance(dist, Counter)
    assert dist["Positive"] == 1
    assert dist["Negative"] == 1
    assert dist["Neutral"] == 1
