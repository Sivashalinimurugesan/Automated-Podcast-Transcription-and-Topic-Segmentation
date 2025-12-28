import torch
from transformers import pipeline
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"

def load_summarizer():
    """Loads the summarization model on GPU if available."""
    # Check if we are already in a streamlit context to avoid re-loading often
    # (Optional optimization, keeping it simple for now)
    
    print("[STATUS] Loading AI Models...")
    
    # --- GPU CHECK ---
    if torch.cuda.is_available():
        device_id = 0
    else:
        device_id = -1
        print("WARNING: GPU not found. Running on CPU.")

    try:
        return pipeline("summarization", model=SUMMARIZATION_MODEL, device=device_id)
    except Exception as e:
        print(f"[WARNING] Summarizer failed to load: {e}")
        return None

def generate_summary(summarizer, text):
    """Generates a summary for a given text segment."""
    if not summarizer:
        return "Summary unavailable"
    
    # Safety: If text is too short, just return the text itself
    if len(text) < 50:
        return text
    
    try:
        # Truncate text to avoid model size limits (simple safety check)
        safe_text = text[:3000] 
        
        # Dynamic length: don't force 60 words if input is only 20 words
        max_len = min(60, len(safe_text.split()))
        min_len = min(10, max_len - 1)
        
        res = summarizer(safe_text, max_length=max_len, min_length=min_len, do_sample=False)
        return res[0]['summary_text']
    except Exception as e:
        print(f"Summarization error: {e}")
        return "Summary unavailable"

if __name__ == "__main__":
    print("--- TESTING SUMMARIZATION ---")
    model = load_summarizer()
    sample_text = "Artificial intelligence (AI) is intelligence demonstrated by machines..."
    print(f"\nSummary: {generate_summary(model, sample_text)}")