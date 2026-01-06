import os
import config
import librosa
import soundfile as sf
from pydub import AudioSegment

def clean_all_audio():
    print(f"[INFO] Looking for files in: {config.RAW_AUDIO_FOLDER}")
    
    if not os.path.exists(config.RAW_AUDIO_FOLDER):
        print(f"[ERROR] Folder not found: {config.RAW_AUDIO_FOLDER}")
        return

    files = [f for f in os.listdir(config.RAW_AUDIO_FOLDER) if f.endswith(('.flac', '.wav', '.mp3'))]

    if not files:
        print(f"[INFO] No files found in {config.RAW_AUDIO_FOLDER}!")
        return

    for filename in files:
        print(f"[PROCESSING] {filename}...")

        input_path = os.path.join(config.RAW_AUDIO_FOLDER, filename)
        file_base_name = os.path.splitext(filename)[0]
        output_wav = os.path.join(config.PROCESSED_FOLDER, f"clean_{file_base_name}.wav") 
        temp_wav = os.path.join(config.PROCESSED_FOLDER, "temp.wav")

        try:
            # 1. Resample
            y, sr = librosa.load(input_path, sr=16000)
            sf.write(temp_wav, y, sr)

            # 2. Normalize
            audio = AudioSegment.from_wav(temp_wav)
            normalized_audio = audio.normalize()

            # 3. Save
            normalized_audio.export(output_wav, format="wav")
            print(f"   [CLEANED] {output_wav}")

        except Exception as e:
            print(f"   [ERROR] {e}")

    if os.path.exists(temp_wav):
        os.remove(temp_wav)

if __name__ == "__main__":
    clean_all_audio()