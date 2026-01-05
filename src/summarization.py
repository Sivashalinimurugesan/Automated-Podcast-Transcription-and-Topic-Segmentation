import os
import glob
import json
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# SETTINGS
# -----------------------------
INPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\transcripts"
OUTPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\summaries"

SUMMARY_SENTENCE_COUNT = 5   # number of sentences in summary


# -----------------------------
# SUMMARIZATION
# -----------------------------
def summarize_text(text, top_n=5):
    sentences = sent_tokenize(text)

    if len(sentences) <= top_n:
        return sentences

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(sentences)

    sentence_scores = tfidf_matrix.sum(axis=1).A1

    top_sentence_indices = np.argsort(sentence_scores)[-top_n:]
    top_sentence_indices = sorted(top_sentence_indices)

    summary = [sentences[i] for i in top_sentence_indices]

    return summary


# -----------------------------
# MAIN
# -----------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    transcript_files = glob.glob(os.path.join(INPUT_DIR, "*.txt"))

    print(f"[INFO] Found {len(transcript_files)} transcript files")

    for path in transcript_files:
        filename = os.path.splitext(os.path.basename(path))[0]
        output_path = os.path.join(OUTPUT_DIR, f"{filename}_summary.json")

        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            print(f"[WARN] Empty file: {filename}.txt — skipping")
            continue

        summary_sentences = summarize_text(text, SUMMARY_SENTENCE_COUNT)

        output_data = {
            "source_file": f"{filename}.txt",
            "summary_sentence_count": len(summary_sentences),
            "summary": summary_sentences
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Saved summary: {output_path}")

    print("\n[INFO] Initial summaries generated successfully.")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
