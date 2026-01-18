import librosa
import numpy as np

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

from audio_preprocessing.preprocess import preprocess_audio
from transcription.transcribe import get_transcription
from segmentation.segmentation import process_segments, extract_keywords

# ===== LOGGING =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== APP =====
app = Flask(__name__)
CORS(app)

# ===== AUDIO SERVE =====
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("data/clean_audio", filename)

# ===== WAVEFORM API =====
@app.route("/waveform/<filename>")
def get_waveform(filename):
    audio_path = os.path.join("data/clean_audio", filename)

    if not os.path.exists(audio_path):
        return jsonify({"error": "Audio file not found"}), 404

    # Load audio
    y, sr = librosa.load(audio_path, sr=None)

    # Downsample for faster response
    y = y[::100]
    time = np.linspace(0, len(y) / sr, num=len(y))

    return jsonify({
        "time": time.tolist(),
        "amplitude": y.tolist()
    })


# ===== PIPELINE =====
@app.route("/upload", methods=["POST"])
def run_pipeline():
    logger.info("--- New Request Received ---")

    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file found"}), 400

        audio_file = request.files["audio"]
        mode = request.form.get("mode", "summarize")

        os.makedirs("data/raw_audio", exist_ok=True)
        os.makedirs("data/clean_audio", exist_ok=True)

        raw_path = os.path.join("data/raw_audio", audio_file.filename)
        audio_file.save(raw_path)

        clean_wav = preprocess_audio(audio_file.filename)

        audio_filename = os.path.basename(clean_wav)
        audio_url = f"http://127.0.0.1:5000/audio/{audio_filename}"

        transcript = get_transcription(clean_wav)
        keywords = extract_keywords(transcript)

        # ==========================
        # TRANSCRIBE ONLY
        # ==========================
        if mode == "transcribe":
            segments = [{
                "start": 0,
                "end": 9999,
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

        # ==========================
        # SUMMARIZE MODE
        # ==========================
        final_segments = process_segments(transcript, clean_wav)

        # ⚠️ ENSURE NUMERIC start/end
        for seg in final_segments:
            seg["start"] = float(seg.get("start", 0))
            seg["end"] = float(seg.get("end", seg["start"] + 10))
            seg["sentiment"] = seg.get("sentiment", "NEUTRAL")

        return jsonify({
            "mode": "summarize",
            "segments": final_segments,
            "audioUrl": audio_url,
            "overall_keywords": keywords
        })

    except Exception as e:
        logger.error(f"FATAL ERROR: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
