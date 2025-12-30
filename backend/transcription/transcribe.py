import whisper
import os

model = whisper.load_model("base")

def get_transcription(clean_wav_path):
    result = model.transcribe(clean_wav_path)
    return result["text"] # Seedha text return