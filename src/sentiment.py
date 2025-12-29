import os
import json
from transformers import pipeline
from src.logger import get_logger

# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------
logger = get_logger("SENTIMENT", "pipeline.log")

# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------
sentiment_model = pipeline("sentiment-analysis")

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
SEGMENTS_DIR = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\segments"
OUTPUT_DIR = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\sentiment"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# SENTIMENT PER SEGMENT
# ---------------------------------------------------------
def analyze_segment_sentiment(text):
    text = text[:512]  # model safety limit
    result = sentiment_model(text)
    return result[0]

# ---------------------------------------------------------
# MAIN PIPELINE STEP
# ---------------------------------------------------------
def run():
    logger.info("Starting sentiment analysis")

    for file in os.listdir(SEGMENTS_DIR):
        if not file.endswith(".json"):
            continue

        input_path = os.path.join(SEGMENTS_DIR, file)
        output_path = os.path.join(
            OUTPUT_DIR, file.replace(".json", "_sentiment.json")
        )

        # Resume-safe
        if os.path.exists(output_path):
            logger.info(f"Skipping already processed file: {file}")
            continue

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for seg in data["segments"]:
            sentiment = analyze_segment_sentiment(seg["segment_text"])
            seg["sentiment"] = sentiment

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logger.info(f"Sentiment saved: {output_path}")

    logger.info("Sentiment analysis completed")

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    run()
