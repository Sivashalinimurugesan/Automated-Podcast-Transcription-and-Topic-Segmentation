import os
from backend.segmentation.segmentation import process_segments

def test_process_segments_returns_segments():
    dummy_text = (
        "This is the first sentence. "
        "This is the second sentence. "
        "This is the third sentence."
    )

    test_wav = "data/clean_audio/test_audio.wav"

    # Skip test if audio file not present
    if not os.path.exists(test_wav):
        return

    segments = process_segments(dummy_text, test_wav)

    # Basic validations
    assert isinstance(segments, list)
    assert len(segments) > 0

    # Validate structure of one segment
    segment = segments[0]

    assert "segment_number" in segment
    assert "start_time" in segment
    assert "end_time" in segment
    assert "text" in segment
    assert "sentiment" in segment
    assert "keywords" in segment
    assert "summary" in segment
