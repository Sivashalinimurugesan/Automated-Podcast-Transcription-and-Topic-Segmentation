import os

# Get the absolute path of the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define absolute paths for data
DATA_FOLDER = os.path.join(BASE_DIR, "data")
RAW_AUDIO_FOLDER = os.path.join(DATA_FOLDER, "raw")
PROCESSED_FOLDER = os.path.join(DATA_FOLDER, "processed")

# Create directories immediately
os.makedirs(RAW_AUDIO_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Settings
SAMPLE_RATE = 16000

# SAFE PRINT (No Emojis)
print(f"[INFO] Configuration loaded. Raw: {RAW_AUDIO_FOLDER}")