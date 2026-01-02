import re
import logging
from jiwer import wer, cer
from sentence_transformers import SentenceTransformer, util

# -------------------------------------------------
# LOGGING SETUP
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("evaluation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("EVALUATION")

# -------------------------------------------------
# LOAD MODEL (ONCE)
# -------------------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------------------------
# TEXT NORMALIZATION
# -------------------------------------------------
def normalize_text(text: str) -> str:
    if not text or not text.strip():
        return ""

    text = text.lower()
    text = re.sub(r"\[[^\]]+\]", "", text)
    text = re.sub(r"\b(d|p):", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# -------------------------------------------------
# QUALITY EVALUATION (UI SAFE)
# -------------------------------------------------
def get_evaluation_summary_for_ui(predicted_text: str, reference_text: str):
    logger.info("Starting evaluation")

    if not reference_text or not reference_text.strip():
        logger.warning("Reference text empty")
        return _default_result()

    pred_clean = normalize_text(predicted_text)
    ref_clean = normalize_text(reference_text)

    if not pred_clean or not ref_clean:
        logger.warning("Normalized text empty")
        return _default_result()

    wer_score = wer(ref_clean, pred_clean)
    cer_score = cer(ref_clean, pred_clean)

    wer_pct = round(wer_score * 100, 2)
    cer_pct = round(cer_score * 100, 2)

    try:
        emb_ref = model.encode(ref_clean, convert_to_tensor=True)
        emb_pred = model.encode(pred_clean, convert_to_tensor=True)
        similarity = util.cos_sim(emb_ref, emb_pred)[0][0].item() * 100
        similarity = round(similarity, 2)
    except Exception:
        similarity = 0.0

    wer_accuracy = max(0, (1 - wer_score) * 100)
    cer_accuracy = max(0, 100 - cer_pct)

    wer_penalty = (wer_pct - 10) * 1.5 if wer_pct > 10 else 0
    cer_penalty = (cer_pct - 8) * 1.2 if cer_pct > 8 else 0

    quality_score = 0.7 * max(0, wer_accuracy - wer_penalty) + \
                    0.3 * max(0, cer_accuracy - cer_penalty)

    if similarity > 80:
        quality_score = min(95, quality_score + (similarity - 80) * 0.25)

    quality_score = round(max(0, min(100, quality_score)), 2)

    return {
        "avg_quality_score": quality_score,
        "avg_wer": wer_pct,
        "avg_cer": cer_pct,
        "avg_similarity": similarity
    }

# -------------------------------------------------
# DEFAULT RESULT
# -------------------------------------------------
def _default_result():
    return {
        "avg_quality_score": 0.0,
        "avg_wer": 100.0,
        "avg_cer": 100.0,
        "avg_similarity": 0.0
    }

# -------------------------------------------------
# HELPER FUNCTION FOR TESTING
# -------------------------------------------------
def compute_accuracy(wer, cer):
    accuracy = 100 - (wer * 0.7 + cer * 0.3)
    return max(70, min(accuracy, 100))

# -------------------------------------------------
# MAIN FUNCTION (ENTRY POINT)
# -------------------------------------------------
def main():
    predicted_text = "The patient has mild fever and headache."
    reference_text = "The patient has mild fever and headache."

    # Call normalization
    clean_pred = normalize_text(predicted_text)
    clean_ref = normalize_text(reference_text)

    # Call evaluation
    evaluation = get_evaluation_summary_for_ui(clean_pred, clean_ref)

    # Call accuracy helper
    accuracy = compute_accuracy(
        evaluation["avg_wer"],
        evaluation["avg_cer"]
    )

    print("Evaluation Result:")
    print(evaluation)
    print(f"Computed Accuracy: {accuracy}%")

# -------------------------------------------------
# PROGRAM START
# -------------------------------------------------
if __name__ == "__main__":
    main()
