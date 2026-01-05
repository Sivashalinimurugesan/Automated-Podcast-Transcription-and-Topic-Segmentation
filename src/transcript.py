import os
import glob
from faster_whisper import WhisperModel

# -----------------------------
# SETTINGS
# -----------------------------
INPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\audio_preprocessed"
OUTPUT_DIR = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\transcripts"

MODEL_SIZE = "small"        # tiny | base | small | medium | large-v2
DEVICE = "cpu"              # "cuda" if NVIDIA GPU available
COMPUTE_TYPE = "int8"       # CPU: int8 | GPU: float16


# -----------------------------
# MAIN
# -----------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    wav_files = glob.glob(os.path.join(INPUT_DIR, "*.wav"))

    if not wav_files:
        raise RuntimeError("No WAV files found in input directory")

    print(f"[INFO] Found {len(wav_files)} WAV files")

    print(f"[INFO] Loading Faster-Whisper model: {MODEL_SIZE}")
    model = WhisperModel(
        MODEL_SIZE,
        device=DEVICE,
        compute_type=COMPUTE_TYPE
    )

    for wav_path in wav_files:
        filename = os.path.splitext(os.path.basename(wav_path))[0]
        output_txt = os.path.join(OUTPUT_DIR, f"{filename}.txt")

        print(f"[INFO] Transcribing: {filename}.wav")

        try:
            segments, info = model.transcribe(
                wav_path,
                beam_size=5,
                language="en"
            )

            transcript = " ".join(segment.text for segment in segments)

            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(transcript.strip())

            print(f"[OK] Saved: {output_txt}")

        except Exception as e:
            print(f"[ERROR] Failed {filename}: {e}")

    print("\n[INFO] All transcriptions completed.")


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
