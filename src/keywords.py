import os
from wordcloud import WordCloud
from src.logger import get_logger

logger = get_logger("KEYWORDS", "pipeline.log")

TRANSCRIPTS_DIR = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\transcripts"
OUTPUT_DIR = r"C:\Users\venka\OneDrive\Desktop\MedicalPodcastAI\graphs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# CORE LOGIC (UNCHANGED)
# ---------------------------------------------------------
def run():
    logger.info("Starting keyword cloud generation")

    for file in os.listdir(TRANSCRIPTS_DIR):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(TRANSCRIPTS_DIR, file), "r", encoding="utf-8") as f:
            text = f.read()

        wc = WordCloud(width=800, height=400).generate(text)

        out_file = file.replace(".txt", "_keyword_cloud.png")
        out_path = os.path.join(OUTPUT_DIR, out_file)

        wc.to_file(out_path)

        logger.info(f"Keyword cloud saved for {file}")

    logger.info("Keyword cloud generation completed")

# ---------------------------------------------------------
# MAIN WRAPPER (FOR PIPELINE CONTROLLER)
# ---------------------------------------------------------
def main():
    run()

# ---------------------------------------------------------
# RUN STANDALONE
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
