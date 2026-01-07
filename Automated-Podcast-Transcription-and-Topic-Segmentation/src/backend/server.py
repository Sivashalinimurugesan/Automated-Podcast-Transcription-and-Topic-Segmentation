import os
import shutil
import subprocess
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure directories exist
os.makedirs(config.RAW_AUDIO_FOLDER, exist_ok=True)
os.makedirs(config.PROCESSED_FOLDER, exist_ok=True)

def force_cleanup(folder_path):
    """
    Blocks execution until the folder is completely empty.
    Retries endlessly until Windows releases the file lock.
    """
    print(f"[CLEANUP] Cleaning {folder_path}...")
    
    # 1. Try to delete everything
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"   [WARNING] Could not delete {filename} yet: {e}")

    # 2. VERIFY it is empty. If not, wait and try again.
    attempts = 0
    while os.path.exists(folder_path) and len(os.listdir(folder_path)) > 0:
        time.sleep(0.5) # Wait 0.5 seconds
        attempts += 1
        print(f"   [WAITING] Waiting for files to clear... ({attempts})")
        
        # Retry delete loop
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path): os.unlink(file_path)
            except: pass
            
        if attempts > 10:
            print("   [ERROR] FORCE BREAK: Windows is refusing to release files. Please restart python.")
            break

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # === NEW SECURITY CHECK ===
    allowed_extensions = {'.mp3', '.wav'}
    # Check if file ends with .mp3 or .wav (case insensitive)
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        print(f"[ERROR] User tried to upload invalid file: {file.filename}")
        return jsonify({"error": "Invalid file type. Only MP3 and WAV are allowed."}), 400
    
    # 1. FORCE CLEAN BOTH FOLDERS
    force_cleanup(config.RAW_AUDIO_FOLDER)
    force_cleanup(config.PROCESSED_FOLDER)

    # ... (Rest of your code remains the same)

    # 2. SAVE NEW FILE
    print(f"[UPLOAD] Saving new file: {file.filename}")
    save_path = os.path.join(config.RAW_AUDIO_FOLDER, file.filename)
    file.save(save_path)

    # 3. RUN PIPELINE
    print("[PIPELINE] Running AI Pipeline...")
    try:
        script = os.path.join(BASE_DIR, "run_pipeline.py")
        
        # Pass the filename to the pipeline explicitly
        my_env = os.environ.copy()
        my_env["TARGET_FILENAME"] = file.filename
        
        result = subprocess.run(
            ["python", "-u", script], 
            check=True, 
            cwd=BASE_DIR,
            env=my_env,
            capture_output=True,
            text=True
        )
        print("Pipeline Output:", result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("Pipeline Error:", e.stderr)
        return jsonify({"error": f"Pipeline failed: {e.stderr}"}), 500
    except Exception as e:
        print("General Error:", str(e))
        return jsonify({"error": str(e)}), 500

    # 4. FIND RESULT
    # There should only be ONE json file now because we wiped the folder
    json_files = [f for f in os.listdir(config.PROCESSED_FOLDER) if f.endswith(".json")]
    
    if not json_files:
        return jsonify({"error": "Pipeline finished but no JSON found."}), 500
    
    # Just take the first one found
    result_path = os.path.join(config.PROCESSED_FOLDER, json_files[0])
    
    try:
        with open(result_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Could not read JSON: {str(e)}"}), 500

  # ... (Keep previous code until step 5)

    # 5. FORMAT FOR FRONTEND
    processed_topics = []
    topics_list = data.get('topics', data) if isinstance(data, dict) else data
    
    if not isinstance(topics_list, list):
        topics_list = []

    for idx, topic in enumerate(topics_list):
        start = topic.get('start_time', f"{idx*2:02d}:00")
        processed_topics.append({
            "topic_id": idx + 1,
            "start_time": start,
            "summary": topic.get('summary', "No summary provided."),
            "keywords": topic.get('keywords', []),
            "sentiment": topic.get('sentiment', 0.0) # <--- Pass Sentiment Score
        })

    return jsonify({"topics": processed_topics})

if __name__ == '__main__':
    # Threaded=False ensures requests process one by one, preventing race conditions
    app.run(port=5000, debug=True, threaded=False)