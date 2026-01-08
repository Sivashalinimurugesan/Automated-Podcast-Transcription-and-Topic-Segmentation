import sys
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import extract_keywords

def test_extract_keywords_basic():
    txt = "fever cough fever infection treatment fever"
    keywords = extract_keywords(txt, k=3)
    assert isinstance(keywords, list)
    assert "fever" in keywords

def test_extract_keywords_empty():
    assert extract_keywords("", k=5) == []
