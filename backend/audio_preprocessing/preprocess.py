import os
from pydub import AudioSegment
import noisereduce as nr
import librosa
import soundfile as sf

# Paths as per your structure
RAW_DIR = "data/raw_audio"
CLEAN_DIR = "data/clean_audio"

def preprocess_audio(file_name):
    input_path = os.path.join(RAW_DIR, file_name)
    
    # 1. Convert to WAV
    sound = AudioSegment.from_file(input_path)
    wav_name = file_name.rsplit('.', 1)[0] + ".wav"
    wav_path = os.path.join(CLEAN_DIR, wav_name)
    
    sound = sound.set_frame_rate(16000).set_channels(1)
    sound.export(wav_path, format="wav")

    # 2. Noise Reduction
    y, sr = librosa.load(wav_path, sr=16000)
    reduced_noise = nr.reduce_noise(y=y, sr=sr)
    sf.write(wav_path, reduced_noise, sr)
    
    return wav_path # Path return karna zaroori hai