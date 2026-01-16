import pytest
from backend.transcription.transcribe import transcribe_audio

def test_transcribe_file_not_found():
    with pytest.raises(FileNotFoundError):
        transcribe_audio("tests/eps7.mp3")
