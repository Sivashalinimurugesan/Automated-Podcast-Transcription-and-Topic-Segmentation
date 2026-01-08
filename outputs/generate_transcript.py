
!pip install -U openai-whisper > /dev/null 2>&1
!apt-get -y install ffmpeg > /dev/null 2>&1

import os
import zipfile
import whisper
import torch
import gc
import pickle
from google.colab import files

#  1. AUTO-FIND ZIP
print(" FINDING EXISTING ZIP...")
existing_zips = [f for f in os.listdir('/content') if f.lower().endswith('.zip')]
if existing_zips:
    zip_path = f'/content/{existing_zips[0]}'
    print(f" USING EXISTING: {zip_path}")
else:
    print(" UPLOAD ZIP (first time only)...")
    uploaded = files.upload()
    zip_path = list(uploaded.keys())[0]

# 2. EXTRACT (skip if done)
if not os.path.exists('/content/audios'):
    print(" EXTRACTING...")
    os.makedirs('/content/audios', exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('/content/audios')
    print(" EXTRACTED")
else:
    print(" ALREADY EXTRACTED")

# FIND folders
audio_files = []
for root, dirs, files_list in os.walk('/content/audios'):
    for file in files_list:
        if file.lower().endswith(('.mp3','.wav','.m4a','.flac','.mp4')):
            audio_files.append(os.path.join(root, file))
print(f" Found {len(audio_files)} files")

#  3. RESUME FROM YOUR PROGRESS!
progress_file = '/content/progress.pkl'
if os.path.exists(progress_file):
    with open(progress_file, 'rb') as f:
        transcripts = pickle.load(f)
    print(f"📋 RESUMING from {len(transcripts)}/{len(audio_files)}")
else:
    transcripts = {}

print(" 4. LOADING MEDIUM MODEL")
device = "cuda" if torch.cuda.is_available() else "cpu"
torch.cuda.empty_cache()
model = whisper.load_model("medium", device=device)
print(" Model loaded")

print(" 5. CONTINUING TRANSCRIPTION...")
new_files = 0
for i, full_path in enumerate(audio_files):
    audio_file = os.path.basename(full_path)

    if audio_file in transcripts:
        if i % 20 == 0:
            print(f"  {i+1}/{len(audio_files)}: {audio_file} (done)")
        continue

    try:
        result = model.transcribe(full_path, fp16=True, language="en")
        transcripts[audio_file] = result["text"]
        new_files += 1
        print(f" {i+1}/{len(audio_files)}: {audio_file}")

        if new_files % 10 == 0:
            with open(progress_file, 'wb') as f:
                pickle.dump(transcripts, f)
            print(f" SAVED at {len(transcripts)}/{len(audio_files)}")

        del result
        torch.cuda.empty_cache()
        gc.collect()

    except Exception as e:
        print(f" Skip {audio_file}: {e}")
        transcripts[audio_file] = ""

# FINAL SAVE
with open(progress_file, 'wb') as f:
    pickle.dump(transcripts, f)

print(" 6. SAVING TRANSCRIPTS...")
os.makedirs('/content/transcripts', exist_ok=True)
for audio_file, text in transcripts.items():
    base_name = os.path.splitext(audio_file)[0]
    txt_path = f'/content/transcripts/{base_name}.txt'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

!zip -r /content/transcripts.zip /content/transcripts/
files.download('/content/transcripts.zip')
print("  COMPLETE! transcripts.zip DOWNLOADING...")

