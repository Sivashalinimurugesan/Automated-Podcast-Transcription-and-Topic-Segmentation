import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transcription import safe_transcribe_file

def test_transcription_function():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    clean_dir = os.path.join(base, "Data_denver", "clean_wav")

    if not os.path.exists(clean_dir):
        return

    files = [f for f in os.listdir(clean_dir) if f.endswith(".wav")]
    if not files:
        return

    audio = os.path.join(clean_dir, files[0])
    result = safe_transcribe_file(audio)

    assert isinstance(result, str)
