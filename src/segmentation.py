import os
import glob
import json
import nltk
from nltk.tokenize import sent_tokenize

# -----------------------------
# SETTINGS
# -----------------------------
INPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\transcripts"
OUTPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\segmented_transcripts"

SENTENCES_PER_SEGMENT = 5   # adjust based on use case


# -----------------------------
# SEGMENTATION
# -----------------------------
def segment_text(text, sentences_per_segment=5):
    sentences = sent_tokenize(text)

    segments = []
    for i in range(0, len(sentences), sentences_per_segment):
        chunk = sentences[i:i + sentences_per_segment]
        segments.append(" ".join(chunk))

    return segments


# -----------------------------
# MAIN
# -----------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    txt_files = glob.glob(os.path.join(INPUT_DIR, "*.txt"))

    if not txt_files:
        raise RuntimeError("No transcript files found")

    print(f"[INFO] Found {len(txt_files)} transcript files")

    for txt_path in txt_files:
        filename = os.path.splitext(os.path.basename(txt_path))[0]
        output_json = os.path.join(OUTPUT_DIR, f"{filename}.json")

        print(f"[INFO] Segmenting: {filename}.txt")

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print(f"[WARN] Empty file: {filename}.txt — skipping")
            continue

        segments = segment_text(text, SENTENCES_PER_SEGMENT)

        data = {
            "source_file": f"{filename}.txt",
            "num_segments": len(segments),
            "segments": [
                {
                    "segment_id": idx + 1,
                    "text": segment
                }
                for idx, segment in enumerate(segments)
            ]
        }

        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Saved: {output_json}")

    print("\n[INFO] All transcripts segmented successfully.")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
