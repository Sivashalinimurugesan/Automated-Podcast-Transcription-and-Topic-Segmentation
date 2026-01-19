from backend.segmentation.segmentation import summarize_segment

def test_summarize_segment_returns_text():
    sample_text = (
        "Artificial intelligence is transforming industries by enabling "
        "machines to learn from data, recognize patterns, and make decisions. "
        "It is widely used in healthcare, finance, education, and media."
    )

    summary = summarize_segment(sample_text)

    # Check output type
    assert isinstance(summary, str)

    # Summary should not be empty
    assert len(summary) > 0

    # Summary length should be <= original text
    assert len(summary) <= len(sample_text)
