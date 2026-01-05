from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
import os
import logging

# Aapke scripts se functions import
from audio_preprocessing.preprocess import preprocess_audio
from transcription.transcribe import get_transcription
from segmentation.segmentation import process_segments, extract_keywords

# 1. Logging Setup (Terminal mein debug dekhne ke liye)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # React connection allow karne ke liye

@app.route('/upload', methods=['POST'])
def run_pipeline():
    logger.info("--- New Request Received ---")
    try:
        # Check karein ki file aayi hai ya nahi
        if 'audio' not in request.files:
            logger.warning("No audio file in request")
            return jsonify({"error": "No audio file found"}), 400
            
        audio_file = request.files['audio']
        mode = request.form.get('mode', 'summarize')
        logger.info(f"File: {audio_file.filename} | Mode: {mode}")

        # Folders create karein agar nahi hain
        os.makedirs("data/raw_audio", exist_ok=True)
        os.makedirs("data/clean_audio", exist_ok=True)

        # Step 1: Raw file save karein
        raw_path = os.path.join("data/raw_audio", audio_file.filename)
        audio_file.save(raw_path)
        logger.info(f"Step 1: Raw file saved at {raw_path}")

        # Step 2: Preprocessing (Noise reduction & WAV conversion)
        logger.info("Step 2: Starting Preprocessing...")
        clean_wav = preprocess_audio(audio_file.filename)
        logger.info(f"Preprocessing complete. Clean file: {clean_wav}")

        # Step 3: Transcription (Whisper AI)
        logger.info("Step 3: Starting Transcription (Whisper AI)...")
        transcript = get_transcription(clean_wav)
        logger.info("Transcription complete.")

        # Keywords nikalna (Dono modes ke liye)
        keywords = extract_keywords(transcript)

        # Mode wise Response
        if mode == "transcribe":
            logger.info("Sending Transcribe-only response.")
            return jsonify({
                "mode": "transcribe",
                "text": transcript,
                "keywords": keywords,
                "segments": []
            })

        # Step 4: Segmentation & Summarization (BART AI)
        logger.info("Step 4: Starting Segmentation & Summarization...")
        final_data = process_segments(transcript, clean_wav)
        logger.info("All processing steps complete. Sending response.")

        return jsonify({
            "mode": "summarize",
            "segments": final_data,
            "overall_keywords": keywords
        })

    except Exception as e:
        logger.error(f"FATAL ERROR in pipeline: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Debug False aur Reloader False taaki server crash na ho
    logger.info("Starting Flask Server on http://127.0.0.1:5000")
    app.run(port=5000, debug=False, use_reloader=False)