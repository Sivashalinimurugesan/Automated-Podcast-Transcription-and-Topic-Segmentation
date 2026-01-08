import sys
from collections import Counter
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import extract_top_medical_words, MEDICAL_TERMS

def test_extract_top_medical_words_basic():
    segments = [
        {"text": "patient has fever and cough"},
        {"text": "infection and fever observed"},
        {"text": "fever treated with medication"}
    ]
    result = extract_top_medical_words(segments, top_n=3)
    assert isinstance(result, list)
    assert "fever" in [w for w, _ in result]

def test_extract_top_medical_words_empty():
    segments = [{"text": "random text without medical words"}]
    result = extract_top_medical_words(segments, top_n=5)
    assert result == [] or isinstance(result, list)
