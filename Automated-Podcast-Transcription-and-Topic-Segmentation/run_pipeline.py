import os
import json
import config
from datetime import datetime
from audio_cleaner import clean_all_audio
from audio_transcriber import transcribe_all_audio
from text_segmenter import segment_all_transcripts
from summarizer import process_summaries

def run_full_pipeline():
    print("\n" + "="*40)
    print(" PIPELINE STARTED")
    print("="*40)
    
    # Step 1: Clean
    print("\n[Step 1/4] [CLEAN] Cleaning Audio...") 
    clean_all_audio()

    # Step 2: Transcribe
    print("\n[Step 2/4] [TRANSCRIBE] Transcribing...")
    transcribe_all_audio()

    # Step 3: Segment
    print("\n[Step 3/4] [SEGMENT] Segmenting...")
    segment_all_transcripts()

    # Step 4: Summarize
    print("\n[Step 4/4] [SUMMARIZE] Processing Summaries...")
    data = process_summaries()
    
    # Save final JSON
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = os.path.join(config.PROCESSED_FOLDER, f"summary_{ts}.json")
    
    with open(out_file, "w") as f:
        json.dump({"topics": data}, f, indent=4)
        
    print(f"\n[DONE] PIPELINE COMPLETE. Result: {out_file}")

if __name__ == "__main__":
    run_full_pipeline()