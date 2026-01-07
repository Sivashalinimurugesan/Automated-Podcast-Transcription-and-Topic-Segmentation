import os
import re
import nltk
from nltk.tokenize import TextTilingTokenizer
import config

# Download required NLTK data quietly
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

def segment_all_transcripts():
    files = [f for f in os.listdir(config.PROCESSED_FOLDER) if f.startswith("transcript_") or f.endswith(".txt")]
    
    # Filter out files that are not transcripts (e.g. segments or summaries)
    files = [f for f in files if "segments" not in f and "summary" not in f]

    for filename in files:
        input_path = os.path.join(config.PROCESSED_FOLDER, filename)
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        print(f"[SEGMENTER] Processing {filename}...")
        
        # 1. Try Standard TextTiling
        tt = TextTilingTokenizer(w=30, k=6)
        segments = []
        try:
            segments = tt.tokenize(text)
        except ValueError:
            # Fallback if text is too short for tiling
            segments = [text]

        # =========================================================
        # 2. FORCE SEGMENTATION FIX (Add this block)
        # If AI found only 1 segment, force split by sentences
        # =========================================================
        if len(segments) < 2:
            print(f"   [INFO] Only 1 segment found. Applying forced split for UI demo...")
            
            # Split text into sentences using Regex (looks for . ! ? followed by space)
            sentences = re.split(r'(?<=[.!?]) +', text)
            
            # If we have enough sentences, chunk them into groups of 5
            if len(sentences) > 5:
                forced_segments = []
                chunk_size = 5 # <--- Change this to make segments longer/shorter
                
                for i in range(0, len(sentences), chunk_size):
                    chunk = " ".join(sentences[i : i + chunk_size])
                    if len(chunk.strip()) > 10:
                        forced_segments.append(chunk)
                
                # If we successfully created multiple chunks, use them
                if len(forced_segments) > 1:
                    segments = forced_segments
        # =========================================================

        # Save segments
        base_name = "segments_" + filename
        output_path = os.path.join(config.PROCESSED_FOLDER, base_name)
        
        with open(output_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments):
                f.write(f"\n=== TOPIC {i+1} ===\n{seg.strip()}\n")
        
        print(f"   [DONE] Created {len(segments)} topics.")