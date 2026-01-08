import sys
from unittest.mock import MagicMock

# Mock Streamlit
sys.modules["streamlit"] = MagicMock()

# Add project root
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app import transcribe_audio_safe

def test_transcribe_audio_safe_invalid():
    # Non-existing file should return empty string
    assert transcribe_audio_safe("non_existing_file.mp3") == ""
