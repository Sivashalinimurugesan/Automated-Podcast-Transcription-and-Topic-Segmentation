# tests/test_transcription.py
from src.transcription import transcribe_audio

def test_transcribe_sample():
    audio_path = "tests/sample_audio.mp3"  # ek chhota sample audio add karo
    result = transcribe_audio(audio_path)
    assert isinstance(result, str)
    assert len(result) > 0

def test_transcribe_nonexistent_file():
    audio_path = "tests/nonexistent.mp3"
    try:
        transcribe_audio(audio_path)
    except FileNotFoundError:
        assert True
    else:
        assert False
