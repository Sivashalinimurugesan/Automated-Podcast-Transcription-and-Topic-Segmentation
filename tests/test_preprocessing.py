import sys
from unittest.mock import MagicMock

# Mock Streamlit
sys.modules["streamlit"] = MagicMock()

# Add project root
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import clean_text, sec_to_mmss, segment_text

def test_clean_text_basic():
    txt = "Hello   world! [noise]"
    assert clean_text(txt) == "Hello world!"

def test_sec_to_mmss_basic():
    assert sec_to_mmss(65) == "01:05"

def test_segment_text_basic():
    txt = "This is sentence one. Sentence two is here. Three is short. Four more. Five here."
    segments = segment_text(txt, size=2)
    assert isinstance(segments, list)
    assert len(segments) == 3  # 5 sentences, chunk size 2 -> 3 chunks
