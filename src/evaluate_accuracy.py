import os
import jiwer
from jiwer import wer, cer

# ==========================================
# 👇 CONFIGURATION: CHECK THESE PATHS 👇
# Folder containing your "Real" (Ground Truth) text files
GROUND_TRUTH_DIR =r"C:\Users\Dell\Downloads\PodcastFillers\Clean_Transcripts"

# Folder containing your "AI Generated" text files
GENERATED_DIR = os.path.join("data", "transcripts")
# ==========================================

def read_text_file(path):
    """Reads a file and cleans it up for fair comparison."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            # Basic normalization (lowercase, remove extra spaces)
            # This ensures "Hello." and "hello" match
            return jiwer.RemovePunctuation()(text.lower().strip())
    except Exception as e:
        print(f"⚠️ Error reading {path}: {e}")
        return ""

def evaluate():
    print(f"🔍 Comparing transcripts from:\n   Ref: {GROUND_TRUTH_DIR}\n   Hyp: {GENERATED_DIR}\n")
    
    # 1. Find matching files (Assuming filenames are identical, e.g., 'ep1.txt')
    gt_files = set(os.listdir(GROUND_TRUTH_DIR))
    gen_files = set(os.listdir(GENERATED_DIR))
    
    # We only check files that exist in BOTH folders
    common_files = sorted(list(gt_files.intersection(gen_files)))
    
    if not common_files:
        print("❌ No matching files found!")
        print("   Make sure the filenames in 'Clean_Transcripts' match the filenames in 'data/transcripts'.")
        return

    total_wer = 0
    count = 0
    
    print(f"{'FILENAME':<40} | {'WER Score':<10} | {'Status'}")
    print("-" * 65)

    for filename in common_files:
        if not filename.endswith(".txt"):
            continue
            
        # Get paths
        gt_path = os.path.join(GROUND_TRUTH_DIR, filename)
        gen_path = os.path.join(GENERATED_DIR, filename)
        
        # Read text
        truth_text = read_text_file(gt_path)
        ai_text = read_text_file(gen_path)
        
        if not truth_text or not ai_text:
            print(f"{filename:<40} | {'N/A':<10} | ⚠️ Empty File")
            continue

        # Calculate Word Error Rate
        error_rate = wer(truth_text, ai_text)
        total_wer += error_rate
        count += 1
        
        # Determine status (Lower WER is better)
        status = "✅ Excellent" if error_rate < 0.1 else "⚠️ Okay" if error_rate < 0.3 else "❌ Poor"
        print(f"{filename:<40} | {error_rate:.2%}      | {status}")

    # Final Summary
    if count > 0:
        avg_wer = total_wer / count
        accuracy = 1.0 - avg_wer
        print("\n" + "="*30)
        print(f"📊 FINAL RESULTS ({count} episodes)")
        print(f"   Average Word Error Rate (WER): {avg_wer:.2%}")
        print(f"   Estimated Accuracy:            {accuracy:.2%}")
        print("="*30)
        
        if avg_wer < 0.20:
            print("🚀 Result: Your transcription pipeline is performing well!")
        else:
            print("🔧 Result: Accuracy is low. Consider using a larger Whisper model (e.g., 'base' or 'small').")

if __name__ == "__main__":
    evaluate()