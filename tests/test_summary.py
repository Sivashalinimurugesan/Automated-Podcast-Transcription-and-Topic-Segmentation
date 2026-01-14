# tests/test_summary.py
from src.summarization import summarize_text

def test_summary_basic():
    text = "Python is a programming language. It is widely used in AI and web development."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_summary_empty():
    text = ""
    summary = summarize_text(text)
    assert summary == ""
