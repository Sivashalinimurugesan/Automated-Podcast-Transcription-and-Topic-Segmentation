import whisper
import torch
import warnings
import os
import streamlit as st

warnings.filterwarnings("ignore")

def get_device():
    """Checks if a GPU is available for faster processing."""
    return "cuda" if torch.cuda.is_available() else "cpu"

# --- CACHING FIX: Loads model once and keeps it in memory ---
@st.cache_resource(show_spinner=False)
def load_whisper_model(model_size):
    """Loads the Whisper model and caches it."""
    device = get_device()
    print(f"[INFO] Loading Whisper '{model_size}' model on {device}...")
    try:
        # fp16=False ensures compatibility with CPUs
        model = whisper.load_model(model_size, device=device)
        return model
    except Exception as e:
        print(f"Model Load Error: {e}")
        return None

def transcribe_audio(audio_path, model_size="tiny"):
    """
    Transcribes audio using the cached Whisper model.
    Now accepts 'model_size' argument from the UI.
    """
    if not os.path.exists(audio_path):
        return "Error: Audio file not found."

    try:
        # Load the specific model size requested by the user
        model = load_whisper_model(model_size)
        
        if model is None:
            return "Error: Failed to load AI model."

        # Perform transcription
        result = model.transcribe(audio_path, fp16=False)
        return result["text"]

    except Exception as e:
        print(f"Transcription Error: {e}")
        return f"Error during transcription: {str(e)}"

if __name__ == "__main__":
    # Test block
    print("Transcription module ready.")