import sys
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import summarize_text

def test_summarize_text_basic():
    text = "Patient is recovering. Symptoms improved. Followup scheduled."
    summary = summarize_text(text, n=2)
    assert isinstance(summary, str)
    # Ensure it has <= 2 sentences
    sentences = [s for s in summary.split(".") if s.strip()]
    assert len(sentences) <= 2
