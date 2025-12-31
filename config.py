import os

# Base project directory (where this config.py lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 AUDIO DIRECTORIES (INSIDE PROJECT)
AUDIO_RAW_DIR = os.path.join(BASE_DIR, "audio_raw")
AUDIO_PROCESSED_DIR = os.path.join(BASE_DIR, "audio_processed")

# 🔹 SEGMENTS DIRECTORY
SEGMENTS_DIR = os.path.join(BASE_DIR, "segments")

# 🔹 OTHER CONFIG
WHISPER_MODEL = "base"
MIN_MEDICAL_TERMS = 5


import os

# Base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Directories
# -----------------------------
AUDIO_RAW_DIR = os.path.join(BASE_DIR, "audio_raw")
AUDIO_PROCESSED_DIR = os.path.join(BASE_DIR, "audio_processed")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
SEGMENTS_DIR = os.path.join(BASE_DIR, "segments")

# Create dirs if missing
for d in [AUDIO_RAW_DIR, AUDIO_PROCESSED_DIR, TRANSCRIPTS_DIR, SEGMENTS_DIR]:
    os.makedirs(d, exist_ok=True)

# -----------------------------
# Processing Config
# -----------------------------
WHISPER_MODEL = "base"
FP16 = False              # REQUIRED on CPU

# -----------------------------
# NLP / Segmentation
# -----------------------------
SENTENCES_PER_SEGMENT = 5
TOP_KEYWORDS = 20
SUMMARY_SENTENCES = 3
MIN_MEDICAL_TERMS = 5
