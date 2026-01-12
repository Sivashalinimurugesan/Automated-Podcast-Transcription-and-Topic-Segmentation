from src.keyword_extraction import extract_keywords

def segment_transcript(
    transcript,
    max_segment_duration=120,   # seconds
    max_sentences=8
):
    """
    Time-aware, sequential segmentation.
    Produces ordered, non-overlapping segments.
    """

    whisper_segments = transcript["segments"]

    segments = []
    current_text = []
    start_time = None
    sentence_count = 0

    for seg in whisper_segments:
        if start_time is None:
            start_time = seg["start"]

        current_text.append(seg["text"])
        sentence_count += 1

        duration = seg["end"] - start_time

        # Decide if we should close the segment
        if (
            duration >= max_segment_duration
            or sentence_count >= max_sentences
        ):
            combined_text = " ".join(current_text)

            segments.append({
                "id": len(segments) + 1,
                "topic": f"Segment {len(segments) + 1}",
                "start": start_time,
                "end": seg["end"],
                "text": combined_text,
                "keywords": extract_keywords(combined_text, top_n=6)
            })

            # Reset
            current_text = []
            start_time = None
            sentence_count = 0

    # Handle leftover text
    if current_text:
        combined_text = " ".join(current_text)
        segments.append({
            "id": len(segments) + 1,
            "topic": f"Segment {len(segments) + 1}",
            "start": start_time,
            "end": whisper_segments[-1]["end"],
            "text": combined_text,
            "keywords": extract_keywords(combined_text, top_n=6)
        })

    return segments
