import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np

# -----------------------------
# Config
# -----------------------------
TARGET_SR = 16000        # target sample rate
SILENCE_TOP_DB = 30      # silence threshold (larger = more trimming)

# -----------------------------
# Load audio
# -----------------------------
def load_audio(path):
    audio, sr = librosa.load(path, sr=None, mono=True)
    return audio, sr

# -----------------------------
# Resample to 16kHz
# -----------------------------
def resample(audio, sr):
    if sr != TARGET_SR:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)
    return audio

# -----------------------------
# Trim silence
# -----------------------------
def trim_silence(audio):
    trimmed, _ = librosa.effects.trim(audio, top_db=SILENCE_TOP_DB)
    return trimmed

# -----------------------------
# Noise reduction
# -----------------------------
def reduce_noise(audio):
    # use first 0.5 seconds as noise reference
    noise_clip = audio[: TARGET_SR // 2]
    return nr.reduce_noise(y=audio, sr=TARGET_SR, y_noise=noise_clip)

# -----------------------------
# Normalize audio
# -----------------------------
def normalize(audio):
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak
    return audio

# -----------------------------
# Save audio
# -----------------------------
import os
import soundfile as sf

def save_audio(path, audio):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, audio, TARGET_SR)

# -----------------------------
# Full preprocessing pipeline
# -----------------------------
def preprocess_audio(input_path, output_path):
    print("Loading...")
    audio, sr = load_audio(input_path)

    print("Resampling...")
    audio = resample(audio, sr)

    print("Trimming silence...")
    audio = trim_silence(audio)

    print("Reducing noise...")
    audio = reduce_noise(audio)

    print("Normalizing...")
    audio = normalize(audio)

    print("Saving cleaned file...")
    save_audio(output_path, audio)

    print("Done:", output_path)

# -----------------------------
# Run directly
# -----------------------------
if __name__ == "__main__":
    input_file = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\audio_raw\1017.mp3"       # your raw audio
    output_file = r"D:\Automated-Podcast-Transcription-and-Topic-Segmentation\audio_preprocessed\1017.wav"

    preprocess_audio(input_file, output_file)