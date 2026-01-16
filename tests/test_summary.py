from backend.segmentation.segmentation import summarize_text

def test_summary_empty_text():
    result = summarize_text("")
    assert result == ""
