from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

# ===== YOUR PROJECT MODULE IMPORTS =====
from audio_preprocessing.preprocess import preprocess_audio
from transcription.transcribe import get_transcription
from segmentation.segmentation import process_segments, extract_keywords

# ===== LOGGING CONFIG =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ===== FLASK APP INIT =====
app = Flask(__name__)
CORS(app)

# ===== SERVE CLEAN AUDIO TO FRONTEND =====
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("data/clean_audio", filename)

# ===== MAIN PIPELINE =====
@app.route("/upload", methods=["POST"])
def run_pipeline():
    logger.info("--- New Request Received ---")

    try:
        # ---------- VALIDATION ----------
        if "audio" not in request.files:
            return jsonify({"error": "No audio file found"}), 400

        audio_file = request.files["audio"]
        mode = request.form.get("mode", "summarize")

        # ---------- FOLDERS ----------
        os.makedirs("data/raw_audio", exist_ok=True)
        os.makedirs("data/clean_audio", exist_ok=True)

        # ---------- SAVE RAW AUDIO ----------
        raw_path = os.path.join("data/raw_audio", audio_file.filename)
        audio_file.save(raw_path)

        # ---------- PREPROCESS ----------
        clean_wav = preprocess_audio(audio_file.filename)

        audio_filename = os.path.basename(clean_wav)
        audio_url = f"http://127.0.0.1:5000/audio/{audio_filename}"

        # ---------- TRANSCRIPTION ----------
        transcript = get_transcription(clean_wav)
        keywords = extract_keywords(transcript)

        # ==================================================
        # TRANSCRIBE ONLY MODE
        # ==================================================
        if mode == "transcribe":
            segments = [{
                "start_time": "00:00",
                "end_time": "Full Audio",
                "text": transcript,
                "keywords": keywords,
                "summary": "",
                "sentiment": "NEUTRAL"
            }]

            return jsonify({
                "mode": "transcribe",
                "segments": segments,
                "audioUrl": audio_url
            })

        # ==================================================
        # TRANSCRIBE + SUMMARIZE MODE
        # ==================================================
        final_segments = process_segments(transcript, clean_wav)

        return jsonify({
            "mode": "summarize",
            "segments": final_segments,
            "audioUrl": audio_url,
            "overall_keywords": keywords
        })

    except Exception as e:
        logger.error(f"FATAL ERROR: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
