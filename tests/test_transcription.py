import os
from backend.transcription.transcribe import get_transcription

def test_get_transcription_returns_text():
    test_wav = "data/clean_audio/test_audio.wav"

    # skip test if audio not present (professional practice)
    if not os.path.exists(test_wav):
        return

    text = get_transcription(test_wav)

    assert isinstance(text, str)
    assert len(text) > 0
