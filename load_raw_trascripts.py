#  BLOCK 1: SETUP + UPLOAD transcripts.zip (OPTIONAL)
!pip install fpdf2 -q
import pandas as pd, numpy as np, os, zipfile, re
from fpdf import FPDF
from google.colab import files
from collections import Counter
from tqdm import tqdm
from pathlib import Path

print(" BLOCK 1: SETUP + UPLOAD...")

# OPTIONAL UPLOAD
print("📤 Upload transcripts.zip? (optional)")
uploaded = files.upload()

# LOAD TRANSCRIPTS (REAL or DUMMY)
summarized_transcripts = {}
if 'transcripts.zip' in uploaded.keys():
    !unzip -q transcripts.zip -d content/ 2>/dev/null
    txt_files = Path('content').rglob('*.txt')
    for i, fp in enumerate(list(txt_files)[:182]):
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                summarized_transcripts[f's{i+1:03d}'] = {'original': f.read()}
        except: pass
    print(f" LOADED {len(summarized_transcripts)} REAL transcripts")
else:
    print(" Using perfect dummy data")

print(" BLOCK 1 COMPLETE!")
