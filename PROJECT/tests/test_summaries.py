import sys
import os
import json

# Allow importing project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from summaries import process_file

def test_summary_generation():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    transcript_dir = os.path.join(base, "transcripts")
    summary_dir = os.path.join(base, "summaries")

    # Skip test safely if no transcripts
    if not os.path.exists(transcript_dir):
        return

    transcripts = [f for f in os.listdir(transcript_dir) if f.endswith(".txt")]
    if not transcripts:
        return

    transcript_path = os.path.join(transcript_dir, transcripts[0])

    # Run summary generation
    process_file(transcript_path)

    # Find any summary file
    if not os.path.exists(summary_dir):
        assert False, "Summary directory not created"

    summary_files = [f for f in os.listdir(summary_dir) if f.endswith(".json")]
    assert len(summary_files) >= 1

    # Validate JSON structure
    summary_path = os.path.join(summary_dir, summary_files[0])
    with open(summary_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "segments" in data
