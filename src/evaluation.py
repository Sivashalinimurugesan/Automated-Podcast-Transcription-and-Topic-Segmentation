import os
import json
import pandas as pd
import re
from jiwer import wer, cer
from sentence_transformers import SentenceTransformer, util
from src.logger import get_logger

# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------
logger = get_logger("EVALUATION", "pipeline.log")

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
REFERENCE_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\Clean_Transcripts"
TRANSCRIPTS_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\transcripts"
SEGMENTS_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\segments"
GRAPHS_FOLDER = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\graphs"
OUTPUT_FILE = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\final_evaluation.xlsx"

# ---------------------------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------------------------------------
# TEXT NORMALIZATION (UNCHANGED)
# ---------------------------------------------------------
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------------------------------------------------------
# LOAD REFERENCE TEXTS
# ---------------------------------------------------------
def load_reference_texts():
    references = {}
    for file in os.listdir(REFERENCE_FOLDER):
        if file.endswith(".txt"):
            file_id = file.replace(".txt", "")
            with open(os.path.join(REFERENCE_FOLDER, file), "r", encoding="utf-8") as f:
                references[file_id] = normalize(f.read())
    return references

# ---------------------------------------------------------
# EXTRACT SENTIMENT FROM SEGMENTS JSON
# ---------------------------------------------------------
def extract_avg_sentiment(segment_json_path):
    if not os.path.exists(segment_json_path):
        return "NA"

    with open(segment_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sentiments = [s["sentiment"]["label"] for s in data["segments"] if "sentiment" in s]

    if not sentiments:
        return "NA"

    return max(set(sentiments), key=sentiments.count)

# ---------------------------------------------------------
# MAIN EVALUATION
# ---------------------------------------------------------
def evaluate_transcripts():

    logger.info("Starting evaluation pipeline")

    reference_texts = load_reference_texts()
    results = []

    for file in os.listdir(TRANSCRIPTS_FOLDER):
        if not file.endswith(".txt"):
            continue

        file_id = file.replace(".txt", "")

        if file_id not in reference_texts:
            continue

        logger.info(f"Evaluating {file}")

        with open(os.path.join(TRANSCRIPTS_FOLDER, file), "r", encoding="utf-8") as f:
            hyp = normalize(f.read())

        ref = reference_texts[file_id]

        # --- Accuracy metrics ---
        word_error_rate = wer(ref, hyp)
        char_error_rate = cer(ref, hyp)

        emb1 = model.encode(ref, convert_to_tensor=True)
        emb2 = model.encode(hyp, convert_to_tensor=True)
        similarity = float(util.cos_sim(emb1, emb2))

        final_accuracy = round(
            (similarity * 0.85 + (1 - word_error_rate) * 0.15) * 100, 2
        )

        # --- New additions ---
        segment_json = os.path.join(SEGMENTS_FOLDER, file_id + ".json")
        keyword_cloud = os.path.join(GRAPHS_FOLDER, file_id + "_keyword_cloud.png")

        avg_sentiment = extract_avg_sentiment(segment_json)

        results.append({
            "File": file,
            "WER (%)": round(word_error_rate * 100, 2),
            "CER (%)": round(char_error_rate * 100, 2),
            "Semantic Similarity": round(similarity, 3),
            "Final Accuracy (%)": final_accuracy,
            "Dominant Sentiment": avg_sentiment,
            "Segment JSON": segment_json,
            "Keyword Cloud": keyword_cloud
        })

    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_FILE, index=False)

    logger.info(f"Evaluation completed → {OUTPUT_FILE}")
    return df

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    evaluate_transcripts()
