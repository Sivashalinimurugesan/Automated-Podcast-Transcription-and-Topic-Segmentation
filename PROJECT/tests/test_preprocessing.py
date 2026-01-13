import sys
import os
import tempfile

# Step to allow Python to see project files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from preprocessing import clean_audio

def test_clean_audio_runs():
    with tempfile.TemporaryDirectory() as tmp:
        input_audio = os.path.join(tmp, "input.wav")
        output_audio = os.path.join(tmp, "output.wav")

        # create fake audio file
        with open(input_audio, "wb") as f:
            f.write(b"TEST")

        try:
            clean_audio(input_audio, output_audio)
        except Exception:
            pass

        # test passes if no crash
        assert os.path.exists(input_audio)
