import re
import logging
from datetime import datetime
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

    # ---------- HARD GUARD ----------
    if not reference_text or not reference_text.strip():
        logger.warning("Reference text empty")
        return _default_result()

    pred_clean = normalize_text(predicted_text)
    ref_clean = normalize_text(reference_text)

    logger.info(f"Pred length: {len(pred_clean)} | Ref length: {len(ref_clean)}")
    logger.info(f"REF SAMPLE: {ref_clean[:150]}")
    logger.info(f"PRED SAMPLE: {pred_clean[:150]}")

    if not pred_clean or not ref_clean:
        logger.warning("Normalized text empty")
        return _default_result()

    # -------------------------------------------------
    # WER / CER (PURE ERROR METRICS)
    # -------------------------------------------------
    wer_score = wer(ref_clean, pred_clean)
    cer_score = cer(ref_clean, pred_clean)

    wer_pct = round(wer_score * 100, 2)
    cer_pct = round(cer_score * 100, 2)

    logger.info(f"WER %: {wer_pct}")
    logger.info(f"CER %: {cer_pct}")

    # -------------------------------------------------
    # SEMANTIC SIMILARITY
    # -------------------------------------------------
    try:
        emb_ref = model.encode(ref_clean, convert_to_tensor=True)
        emb_pred = model.encode(pred_clean, convert_to_tensor=True)
        similarity = util.cos_sim(emb_ref, emb_pred)[0][0].item() * 100
        similarity = round(similarity, 2)
    except Exception as e:
        logger.error(f"Similarity error: {e}")
        similarity = 0.0

    logger.info(f"Semantic Similarity: {similarity}%")

    # -------------------------------------------------
    # QUALITY SCORE (NOT ACCURACY)
    # -------------------------------------------------
    wer_accuracy = max(0, (1 - wer_score) * 100)
    cer_accuracy = max(0, 100 - cer_pct)

    # penalties
    wer_penalty = 0
    if wer_pct > 20:
        wer_penalty = min(50, (wer_pct - 20) * 2)
    elif wer_pct > 10:
        wer_penalty = (wer_pct - 10) * 1.5

    cer_penalty = 0
    if cer_pct > 15:
        cer_penalty = min(40, (cer_pct - 15) * 2)
    elif cer_pct > 8:
        cer_penalty = (cer_pct - 8) * 1.2

    wer_weighted = max(0, wer_accuracy - wer_penalty)
    cer_weighted = max(0, cer_accuracy - cer_penalty)

    quality_score = 0.7 * wer_weighted + 0.3 * cer_weighted

    if similarity > 80:
        quality_score = min(95, quality_score + (similarity - 80) * 0.25)

    quality_score = round(max(0, min(100, quality_score)), 2)

    logger.info(f"Quality Score: {quality_score}")

    # -------------------------------------------------
    # SANITY CHECK (CRITICAL)
    # -------------------------------------------------
    if similarity > 85 and wer_pct > 50:
        logger.warning("⚠ High similarity + high WER → reference mismatch suspected")

    # -------------------------------------------------
    # FINAL RESULT (UI CONTRACT)
    # -------------------------------------------------
    return {
        "avg_quality_score": quality_score,   # renamed (important)
        "avg_wer": wer_pct,                   # PURE error %
        "avg_cer": cer_pct,                   # PURE error %
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
# LOCAL TEST
# -------------------------------------------------
if __name__ == "__main__":
    text = "The patient has mild fever and headache."
    result = get_evaluation_summary_for_ui(text, text)
    print(result)
