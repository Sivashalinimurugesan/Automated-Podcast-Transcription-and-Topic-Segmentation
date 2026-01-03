import sys
import os

# Mock Logger
class MockLogger:
    def info(self, msg): print(f"[INFO] {msg}")
    def warning(self, msg): print(f"[WARN] {msg}")
    def error(self, msg): print(f"[ERROR] {msg}")

# Mock pytorch/pipeline if missing for basic logic test
try:
    import torch
    import pyannote.audio
    print("Dependencies present.")
except ImportError:
    print("Dependencies missing (expected in this dummy env if not installed).")

# We want to test the merging logic specifically, as we can't easily mock the full HF download in a headless test without a real token.
# So we will import the Transcriber class and test `assign_speakers`.

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from transcription import Transcriber

def test_speaker_assignment():
    t = Transcriber(model_size="tiny", compute_type="float32") # Tiny for speed, though we won't load it really if we mock
    
    # Mock Transcript Segments
    # 0-10s: Speaker A
    # 10-20s: Speaker B
    transcript_segments = [
        {"start": 0.0, "end": 5.0, "text": "Hello world."},
        {"start": 5.0, "end": 10.0, "text": "This is me."},
        {"start": 10.0, "end": 15.0, "text": "And now me."},
        {"start": 15.0, "end": 20.0, "text": "Goodbye."}
    ]
    
    # Mock Diarization Segments
    # Overlap logic test
    speaker_segments = [
        {"start": 0.0, "end": 9.0, "speaker": "SPEAKER_A"},
        {"start": 9.5, "end": 20.0, "speaker": "SPEAKER_B"}
    ]
    
    print("\nRunning Assignment Logic...")
    result = t.assign_speakers(transcript_segments, speaker_segments)
    
    for r in result:
        print(f"[{r['start']}-{r['end']}] {r['text']} -> {r['speaker']}")
        
    # Validation
    assert result[0]['speaker'] == "SPEAKER_A" # 0-5 overlaps 0-9
    assert result[1]['speaker'] == "SPEAKER_A" # 5-10 overlaps 0-9 (4s) vs 9.5-20 (0.5s) -> A
    assert result[2]['speaker'] == "SPEAKER_B" # 10-15 overlaps 9.5-20
    assert result[3]['speaker'] == "SPEAKER_B" # 15-20 overlaps 9.5-20
    
    print("\n✅ Speaker assignment logic verified.")

if __name__ == "__main__":
    test_speaker_assignment()
