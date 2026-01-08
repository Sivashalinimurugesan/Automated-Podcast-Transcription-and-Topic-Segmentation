import sys
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import process_transcript

def test_process_transcript_basic():
    text = "Patient has fever. Followup recommended. Medication prescribed."
    duration = 60  # seconds
    segments = process_transcript(text, duration)
    assert isinstance(segments, list)
    assert all("text" in s and "keywords" in s and "summary" in s for s in segments)
