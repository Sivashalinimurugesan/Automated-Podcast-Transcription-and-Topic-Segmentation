import os
import re
import logging
from jiwer import wer, cer
from sentence_transformers import SentenceTransformer, util

# -------------------------------
# Logging setup
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("evaluation.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EVALUATION")

# -------------------------------
# Load sentence transformer model
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# Text normalization
# -------------------------------
def normalize_text(text: str) -> str:
    # Convert to lowercase and remove symbols
    if not text or not text.strip():
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Load clean transcripts
# -------------------------------
def load_clean_transcripts(folder="clean_transcripts"):
    # Read all reference transcripts
    references = {}

    if not os.path.exists(folder):
        logger.warning("Clean transcripts folder not found")
        return references

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_id = filename.replace(".txt", "")
            path = os.path.join(folder, filename)

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read().strip()

                if content:
                    references[file_id] = normalize_text(content)
                else:
                    logger.warning(f"Empty transcript skipped: {filename}")

            except Exception as e:
                logger.warning(f"Unreadable transcript skipped: {filename}")

    logger.info(f"Loaded {len(references)} clean transcripts")
    return references

# -------------------------------
# Semantic similarity
# -------------------------------
def semantic_similarity(text_a: str, text_b: str) -> float:
    # Compute meaning-based similarity
    emb1 = model.encode(text_a, convert_to_tensor=True)
    emb2 = model.encode(text_b, convert_to_tensor=True)
    return round(util.cos_sim(emb1, emb2)[0][0].item() * 100, 2)

# -------------------------------
# Quality evaluation
# -------------------------------
def get_evaluation_summary_for_ui(
    predicted_text: str,
    file_id: str | None = None,
    clean_folder="clean_transcripts"
):
    # Main evaluation function
    logger.info("Starting evaluation")

    pred_clean = normalize_text(predicted_text)
    if not pred_clean:
        return _default_result()

    clean_refs = load_clean_transcripts(clean_folder)

    best_ref_text = None
    best_similarity = -1.0

    # Use exact reference if available
    if file_id and file_id in clean_refs:
        best_ref_text = clean_refs[file_id]
        best_similarity = semantic_similarity(best_ref_text, pred_clean)

    # Otherwise find best match
    else:
        for ref_text in clean_refs.values():
            sim = semantic_similarity(ref_text, pred_clean)
            if sim > best_similarity:
                best_similarity = sim
                best_ref_text = ref_text

    # Compute metrics
    if best_ref_text:
        wer_pct = round(wer(best_ref_text, pred_clean) * 100, 2)
        cer_pct = round(cer(best_ref_text, pred_clean) * 100, 2)

        accuracy = (
            0.65 * best_similarity +
            0.35 * (100 - wer_pct)
        )
        accuracy = round(min(100, max(0, accuracy)), 2)

    # Fallback if no references
    else:
        best_similarity = semantic_similarity(pred_clean, pred_clean)
        wer_pct = 0.0
        cer_pct = 0.0
        accuracy = round(best_similarity, 2)

    return {
        "avg_quality_score": accuracy,
        "avg_similarity": best_similarity,
        "avg_wer": wer_pct,
        "avg_cer": cer_pct
    }

# -------------------------------
# Default result
# -------------------------------
def _default_result():
    # Returned for empty input
    return {
        "avg_quality_score": 0.0,
        "avg_similarity": 0.0,
        "avg_wer": 100.0,
        "avg_cer": 100.0
    }

# -------------------------------
# Local testing
# -------------------------------
def main():
    print(
        get_evaluation_summary_for_ui(
            "patient has head pain and mild fever",
            file_id="GEN0001"
        )
    )

    print(
        get_evaluation_summary_for_ui(
            "patient feels dizzy and nauseous",
            file_id="UNKNOWN_FILE"
        )
    )

if __name__ == "__main__":
    main()
