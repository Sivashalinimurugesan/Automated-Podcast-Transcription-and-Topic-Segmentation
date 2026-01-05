import os
import glob
import json
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# SETTINGS
# -----------------------------
INPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\segmented_transcripts"
OUTPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\keywords"

TOP_K_KEYWORDS = 5
MAX_KEYWORD_REUSE = 2   # max times a keyword can appear across segments


# -----------------------------
# KEYWORD EXTRACTION
# -----------------------------
def extract_keywords_tfidf(segments, top_k=5):
    texts = [seg["text"] for seg in segments]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_df=0.85,      # suppress very common terms
        min_df=1
    )

    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    keyword_usage = defaultdict(int)
    keywords_per_segment = []

    for idx, row in enumerate(tfidf_matrix):
        scores = row.toarray()[0]
        sorted_indices = scores.argsort()[::-1]

        keywords = []

        for i in sorted_indices:
            if scores[i] <= 0:
                break

            word = feature_names[i]

            # suppress overused keywords
            if keyword_usage[word] >= MAX_KEYWORD_REUSE:
                continue

            keywords.append(word)
            keyword_usage[word] += 1

            if len(keywords) == top_k:
                break

        keywords_per_segment.append({
            "segment_id": segments[idx]["segment_id"],
            "keywords": keywords
        })

    return keywords_per_segment


# -----------------------------
# MAIN
# -----------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    json_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))

    print(f"[INFO] Found {len(json_files)} segmented files")

    for json_path in json_files:
        filename = os.path.splitext(os.path.basename(json_path))[0]
        output_path = os.path.join(OUTPUT_DIR, f"{filename}_keywords.json")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        segments = data["segments"]

        keywords = extract_keywords_tfidf(segments, TOP_K_KEYWORDS)

        output_data = {
            "source_file": data["source_file"],
            "num_segments": data["num_segments"],
            "keywords_per_segment": keywords
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Saved keywords: {output_path}")

    print("\n[INFO] Keyword extraction completed.")


if __name__ == "__main__":
    main()
