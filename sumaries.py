# 1. FAST SUMMARIZATION (T5-small + GPU)
print("\n LOADING FAST SUMMARIZER...")
tokenizer = AutoTokenizer.from_pretrained("t5-small")
summarizer = pipeline("summarization", model="t5-small", tokenizer=tokenizer,
                     device=0 if torch.cuda.is_available() else -1)

summary_root = "summaries"
os.makedirs(summary_root, exist_ok=True)

def process_file(in_path):
    try:
        with open(in_path, "r", encoding="utf-8") as f: text = f.read().strip()
        if len(text) < 150: return os.path.basename(in_path), "Too short for summary.", False

        # First 500 words
        words = text.split()[:500]
        summary = summarizer(" ".join(words), max_length=100, min_length=25,
                           truncation=True, do_sample=False)[0]['summary_text']

        # Save individual files
        rel_path = os.path.relpath(in_path, output_root)
        base_name = os.path.splitext(rel_path)[0]
        txt_out = os.path.join(summary_root, f"{base_name}.txt")
        pdf_out = os.path.join(summary_root, f"{base_name}.pdf")
        os.makedirs(os.path.dirname(txt_out), exist_ok=True)

        # TXT
        with open(txt_out, "w") as f: f.write(summary)

        # PDF
        c = canvas.Canvas(pdf_out, pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, f"Summary: {os.path.basename(in_path)}")
        c.setFont("Helvetica", 11)
        y = 720
        for word in summary.split():
            if len(word) > 80: word = word[:77] + "..."
            if y < 60: c.showPage(); y = 750
            c.drawString(50, y, word); y -= 14
        c.save()

        return os.path.basename(in_path), summary, True
    except: return os.path.basename(in_path), "", False

# 2. PARALLEL SUMMARIZATION
print(f"\n SUMMARIZING {len(cleaned_files)} FILES (parallel)...")
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(process_file, path) for path in cleaned_files]
    success_count = 0
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        name, _, success = future.result()
        print(f"[{i}/{len(cleaned_files)}] {'' if success else ''} {name}")
        if success: success_count += 1

print(f"\n {success_count}/{len(cleaned_files)} SUMMARIES COMPLETE!")

# 3. COMBINED TXT + PDF
print("\n CREATING COMBINED FILES...")
summary_files = sorted(glob.glob(os.path.join(summary_root, "**", "*.txt"), recursive=True))

# COMBINED TXT
with open("ALL_SUMMARIES.txt", "w", encoding="utf-8") as out:
    out.write(f"FULL SUMMARY REPORT - {len(summary_files)} TRANSCRIPTS\n{'='*80}\n\n")
    for i, f in enumerate(summary_files, 1):
        with open(f, "r") as sf: text = sf.read()
        out.write(f"[{i}] {os.path.basename(f)}\n{'-'*60}\n{text}\n\n")

# COMBINED PDF
c = canvas.Canvas("ALL_SUMMARIES.pdf", pagesize=letter)
y = 750
c.setFont("Helvetica-Bold", 22); c.drawString(50, y, "COMPLETE TRANSCRIPT SUMMARY"); y -= 50
c.setFont("Helvetica", 14); c.drawString(50, y, f"{len(summary_files)} files processed"); y -= 60

for i, f in enumerate(summary_files, 1):
    with open(f, "r") as sf: text = sf.read()

    if y < 120: c.showPage(); y = 750
    c.setFont("Helvetica-Bold", 13); c.drawString(50, y, f"[{i}] {os.path.basename(f)}"); y -= 25
    c.setFont("Helvetica", 10)

    for line in text.splitlines():
        words = line.split()
        if not words: y -= 12; continue
        current = ""
        for word in words:
            if len(current + word) > 85:
                c.drawString(50, y, current.strip()); y -= 14
                current = word + " "
            else: current += word + " "
        if current: c.drawString(50, y, current.strip()); y -= 14
    y -= 15

c.save()

# 4. ALL DOWNLOADS
print("\n DOWNLOADING EVERYTHING...")

# Individual zips
!zip -qr cleaned.zip transcripts_cleaned
!zip -qr summaries_individual.zip summaries
!zip -qr complete_package.zip cleaned.zip summaries_individual.zip ALL_SUMMARIES.txt ALL_SUMMARIES.pdf

# Download all
files.download("ALL_SUMMARIES.txt")
files.download("ALL_SUMMARIES.pdf")
files.download("cleaned.zip")
files.download("summaries_individual.zip")
files.download("complete_package.zip")

print("\n PIPELINE COMPLETE! DOWNLOADED 5 FILES:")
print("1. ALL_SUMMARIES.txt      ← ALL summaries combined (text)")
print("2. ALL_SUMMARIES.pdf      ← ALL summaries combined (PDF)")
print("3. cleaned.zip            ← 181 cleaned transcripts")
print("4. summaries_individual.zip ← 181 individual summaries (txt+pdf)")
print("5. complete_package.zip   ← Everything zipped")
