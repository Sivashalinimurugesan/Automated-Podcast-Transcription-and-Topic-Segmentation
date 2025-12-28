import json
import warnings
import pandas as pd
import os
import sys
from nltk.tokenize import TextTilingTokenizer

warnings.filterwarnings("ignore")

# ==========================================
# IMPORT HELPERS (Safe Import for UI & Script)
# ==========================================
try:
    # Try importing as if running from root (Streamlit way)
    from src.summarization import load_summarizer, generate_summary
    from src.keyword_extraction import extract_keywords
except ImportError:
    try:
        # Try importing as if running locally (Script way)
        from summarization import load_summarizer, generate_summary
        from keyword_extraction import extract_keywords
    except ImportError:
        pass # Handle inside functions if needed

# ==========================================
# CORE FUNCTIONS
# ==========================================
def create_word_timeline(segments_json):
    """Parses Whisper JSON to create a word-level timeline."""
    try:
        raw_segments = json.loads(segments_json)
        word_timeline = []
        
        for seg in raw_segments:
            text_words = seg['text'].split()
            if not text_words: continue
            
            duration = seg['end'] - seg['start']
            time_per_word = duration / len(text_words)
            
            for i, word in enumerate(text_words):
                w_start = seg['start'] + (i * time_per_word)
                w_end = w_start + time_per_word
                word_timeline.append({
                    "word": word,
                    "start": w_start,
                    "end": w_end
                })
        return word_timeline
    except Exception:
        return []

def load_segmenter():
    """Returns the TextTiling tokenizer."""
    return TextTilingTokenizer(w=30, k=6)

def segment_text(segmenter, full_text):
    """Splits full text into topic segments."""
    try:
        formatted = full_text.replace(". ", ".\n\n")
        return segmenter.tokenize(formatted)
    except ValueError:
        return [full_text]

# ==========================================
# NEW FUNCTION: REQUIRED FOR STREAMLIT UI
# ==========================================
def segment_transcript(full_text):
    """
    Called by ui_app.py to process a single live transcript.
    Input: "This is the full text..."
    Output: List of dicts with 'start', 'end', 'topic', 'text', 'summary'
    """
    segmenter = load_segmenter()
    
    # Load Summarizer (Fixed Import Logic)
    try:
        from src.summarization import load_summarizer
    except ImportError:
        from summarization import load_summarizer
        
    summarizer = load_summarizer() 
    
    # 1. Segment Text
    segments = segment_text(segmenter, full_text)
    
    final_segments = []
    current_time = 0.0
    chars_per_sec = 15 # Estimate time (since UI might not have JSON timings)

    for i, seg_text in enumerate(segments):
        clean_text = seg_text.replace("\n", " ").strip()
        if not clean_text: continue

        # 2. Estimate Time (Fallback for live UI)
        duration = len(clean_text) / chars_per_sec
        start = current_time
        end = current_time + duration
        current_time = end

        # 3. Intelligence
        summary = generate_summary(summarizer, clean_text)
        keywords = extract_keywords(clean_text)
        topic_title = keywords[0].title() if keywords else f"Topic {i+1}"

        final_segments.append({
            "index": i,
            "start": start,
            "end": end,
            "text": clean_text,
            "topic": topic_title,
            "summary": summary,
            "keywords": keywords
        })
    
    return final_segments

# ==========================================
# MAIN EXECUTION BLOCK (Batch CSV Processing)
# ==========================================
if __name__ == "__main__":
    # 1. Setup paths to allow importing sibling modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    sys.path.append(project_root)
    
    # 3. Define File Paths
    input_csv = os.path.join(project_root, "transcripts", "clean_transcripts.csv")
    output_csv = os.path.join(project_root, "segments", "final_search_index.csv")

    if not os.path.exists(input_csv):
        print(f"Error: Transcript file not found at {input_csv}")
        print("Please run 'python src/transcription.py' first.")
        sys.exit()

    print(f"Loading Intelligence Models...")
    segmenter = load_segmenter()
    # Safe load for script execution
    try:
        from src.summarization import load_summarizer
    except ImportError:
        from summarization import load_summarizer
    summarizer = load_summarizer()
    
    print(f"Reading transcripts from: {input_csv}")
    df = pd.read_csv(input_csv)
    
    final_rows = []

    # 4. Process Each Transcript
    for index, row in df.iterrows():
        filename = row['filename']
        print(f"Processing: {filename}...", end="\r")
        
        # A. Create Timeline
        if 'segments_json' not in row or pd.isna(row['segments_json']): continue
        timeline = create_word_timeline(row['segments_json'])
        if not timeline: continue

        # B. Segment Text
        full_text = row['ai_text']
        segments = segment_text(segmenter, full_text)
        
        current_idx = 0
        
        for i, seg_text in enumerate(segments):
            clean_text = seg_text.replace("\n", " ").strip()
            words = clean_text.split()
            if not words: continue
            
            # C. Align Time
            seg_len = len(words)
            start_time = timeline[current_idx]['start'] if current_idx < len(timeline) else 0
            end_idx = min(current_idx + seg_len, len(timeline) - 1)
            end_time = timeline[end_idx]['end'] if timeline else 0
            
            # D. Summarize & Extract Keywords
            summary = generate_summary(summarizer, clean_text)
            keywords = extract_keywords(clean_text)
            
            # E. Format Time String (MM:SS)
            start_str = f"{int(start_time//60):02d}:{int(start_time%60):02d}"
            end_str = f"{int(end_time//60):02d}:{int(end_time%60):02d}"

            final_rows.append({
                "filename": filename,
                "topic_id": i + 1,
                "start_time": start_str,
                "end_time": end_str,
                "start_seconds": int(start_time),
                "end_seconds": int(end_time),
                "summary": summary,
                "keywords": keywords,
                "full_text": clean_text
            })
            
            current_idx += seg_len

    # 5. Save Final Database
    if final_rows:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        pd.DataFrame(final_rows).to_csv(output_csv, index=False)
        print(f"\nSuccess! Final database saved to: {output_csv}")
    else:
        print("\nWarning: No segments generated.")