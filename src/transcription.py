import os
import sys
import whisper

# Fix import path to work from any directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logger import get_logger

# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------
logger = get_logger("TRANSCRIPTION", "pipeline.log")

# ---------------------------------------------------------
# 1. MODEL SELECTION
# ---------------------------------------------------------
MODEL_NAME = "base"

logger.info(f"Loading Whisper Model: {MODEL_NAME} ...")
model = whisper.load_model(MODEL_NAME)
logger.info("Whisper model loaded successfully")

# ---------------------------------------------------------
# 2. FOLDER PATHS (Batch Mode)
# ---------------------------------------------------------
INPUT_FOLDER = r"C:\Users\Venka\OneDrive\Desktop\MedicalPodcastAI\Data\audio_processed"
OUTPUT_FOLDER = r"C:\Users\Venka\OneDrive\Desktop\MedicalPodcastAI\transcripts"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------------------------------------------------
# 3. TIMESTAMP FORMAT
# ---------------------------------------------------------
def format_timestamp(seconds):
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins:02d}:{secs:05.2f}"

# ---------------------------------------------------------
# 4. SIMPLE D / P HEURISTIC (UNCHANGED)
# ---------------------------------------------------------
def infer_speaker(text, previous_was_doctor):
    """
    Simple conversational heuristic:
    - Questions → Doctor
    - Answers → Patient
    """
    if "?" in text:
        return "D"
    return "P" if previous_was_doctor else "D"

# =========================================================
# 5A. TRANSCRIBE SINGLE AUDIO (UI / BACKEND USE)
# =========================================================
def transcribe_single_audio(audio_path):
    """
    Transcribe ONE audio file.
    Used by Flask / UI pipeline.
    Returns transcript as string.
    """

    logger.info(f"Transcribing single audio file: {audio_path}")

    try:
        result = model.transcribe(audio_path, fp16=False, language="en")
    except Exception as e:
        logger.error(f"Transcription failed for {audio_path}: {str(e)}")
        raise

    previous_speaker = "D"
    lines = []

    for seg in result["segments"]:
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"].strip()

        speaker = infer_speaker(text, previous_speaker == "D")
        previous_speaker = speaker

        lines.append(f"[{start} - {end}] {speaker}: {text}")

    return "\n".join(lines)

# =========================================================
# 5B. TRANSCRIBE FILE AND SAVE (BATCH MODE)
# =========================================================
def transcribe_file(audio_path, output_path):
    logger.info(f"Starting transcription: {audio_path}")

    transcript_text = transcribe_single_audio(audio_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    logger.info(f"Transcript saved: {output_path}")

# ---------------------------------------------------------
# 6. SAFE RESUME MAIN (BATCH)
# ---------------------------------------------------------
def main():
    logger.info("Starting batch transcription (timestamps + D/P enabled)")

    count_done = 0
    count_skipped = 0

    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith(".wav"):
            continue

        file_path = os.path.join(INPUT_FOLDER, filename)
        output_name = filename.replace(".wav", ".txt")
        output_txt = os.path.join(OUTPUT_FOLDER, output_name)

        # Resume logic
        if os.path.exists(output_txt):
            logger.info(f"Skipping already processed file: {filename}")
            count_skipped += 1
            continue

        try:
            transcribe_file(file_path, output_txt)
            count_done += 1
        except Exception:
            logger.error(f"Stopping pipeline due to failure at file: {filename}")
            break

    logger.info("Transcription stage completed")
    logger.info(f"New transcripts generated: {count_done}")
    logger.info(f"Files skipped (already processed): {count_skipped}")
    logger.info(f"Output folder: {OUTPUT_FOLDER}")

# ---------------------------------------------------------
# RUN (Batch Mode)
# ---------------------------------------------------------
if __name__ == "__main__":
    main()