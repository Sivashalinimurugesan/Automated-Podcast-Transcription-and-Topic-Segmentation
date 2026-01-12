import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np
import os

def preprocess_audio(audio_path, output_dir="audio_processed"):
    os.makedirs(output_dir, exist_ok=True)

    y, sr = librosa.load(audio_path, sr=16000)

    # Noise reduction
    reduced_noise = nr.reduce_noise(y=y, sr=sr)

    # Remove silence
    intervals = librosa.effects.split(reduced_noise, top_db=30)
    cleaned_audio = np.concatenate([reduced_noise[start:end] for start, end in intervals])

    output_path = os.path.join(output_dir, os.path.basename(audio_path).replace(".", "_cleaned."))
    sf.write(output_path, cleaned_audio, sr)

    return output_path
