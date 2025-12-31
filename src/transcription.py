import os
import whisper
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import AUDIO_PROCESSED_DIR as AUDIO_DIR, TRANSCRIPTS_DIR as OUTPUT_DIR, WHISPER_MODEL as MODEL_NAME, FP16

# ---------------------------------------------------------
# 1. MODEL LOADING
# ---------------------------------------------------------
def load_model(name="medium"):
    """Load Whisper ASR model."""
    print(f"Loading model: {name} ...")
    model = whisper.load_model(name)
    print("Model loaded.\n")
    return model


# ---------------------------------------------------------
# 2. TRANSCRIBE SINGLE FILE
# ---------------------------------------------------------
def transcribe_file(model, input_path, output_path):
    """Transcribe one audio file and save text."""
    print(f"Transcribing: {input_path}")

    result = model.transcribe(input_path)
    text = result["text"]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved → {output_path}\n")


# ---------------------------------------------------------
# 3. GET AUDIO FILE LIST
# ---------------------------------------------------------
def get_audio_files(audio_dir, extensions):
    """Return list of valid audio file paths."""
    return [
        os.path.join(audio_dir, f)
        for f in os.listdir(audio_dir)
        if f.lower().endswith(extensions)
    ]


# ---------------------------------------------------------
# 4. ENSURE OUTPUT DIRECTORY
# ---------------------------------------------------------
def ensure_output_dir(path):
    """Create output directory if missing."""
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------
# 5. MAIN CONTROLLER FUNCTION
# ---------------------------------------------------------
def main():
    from config import AUDIO_PROCESSED_DIR as AUDIO_DIR, TRANSCRIPTS_DIR as OUTPUT_DIR, WHISPER_MODEL as MODEL_NAME, FP16

    audio_extensions = (".wav", ".mp3", ".m4a", ".flac")

    ensure_output_dir(OUTPUT_DIR)

    model = load_model(MODEL_NAME)

    audio_files = get_audio_files(AUDIO_DIR, audio_extensions)

    print("Starting transcription...\n")

    for audio_path in audio_files:
        for audio_path in audio_files:
           from config import TRANSCRIPTS_DIR

    file_name = os.path.splitext(os.path.basename(audio_path))[0]  # remove extension
    output_path = os.path.join(TRANSCRIPTS_DIR, file_name + ".txt")

    transcribe_file(model, audio_path, output_path)


    print("🎉 All files transcribed!")


# ---------------------------------------------------------
# 6. ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
