import os
import whisper
import config
import warnings

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

def transcribe_all_audio():
    # Ensure raw audio folder exists
    if not os.path.exists(config.RAW_AUDIO_FOLDER):
        print(f"[ERROR] Raw audio folder not found: {config.RAW_AUDIO_FOLDER}")
        return

    # Load Whisper Model
    print("[INFO] Loading Whisper model (base)...")
    try:
        model = whisper.load_model("base")
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return

    # Process files
    files = [f for f in os.listdir(config.RAW_AUDIO_FOLDER) if f.endswith(('.mp3', '.wav', '.m4a'))]
    
    if not files:
        print("[INFO] No audio files found to transcribe.")
        return

    print(f"[INFO] Found {len(files)} files to transcribe.")

    for filename in files:
        file_path = os.path.join(config.RAW_AUDIO_FOLDER, filename)
        
        try:
            print(f"[START] Transcribing: {filename}...")
            
            # Run Transcription
            result = model.transcribe(file_path, fp16=False)
            transcript_text = result['text']
            
            # Save to text file
            base_name = os.path.splitext(filename)[0] + ".txt"
            save_path = os.path.join(config.PROCESSED_FOLDER, base_name)
            
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)
            
        # [FIX] I removed the emoji that was here. Now it just says [SUCCESS]
            print(f"[SUCCESS] Saved Transcript: {base_name}")
            
        except Exception as e:
            # [FIX] I removed the emoji that was here. Now it just says [ERROR]
            print(f"[ERROR] Failed to transcribe {filename}: {e}")

if __name__ == "__main__":
    transcribe_all_audio()