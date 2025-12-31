#  BLOCK 3: COMBINED FILES + DOWNLOAD ALL 6 FILES
print(" BLOCK 3: COMBINED FILES + DOWNLOAD...")

# Combined TXT files
with open('ALL_182_STATEMENTS.txt','w') as f:
    f.write("ALL 182 CAREER STATEMENTS\n"+"="*60+"\n\n")
    for i, row in df.iterrows(): f.write(f"{i+1:3d}. {row.statement}\n\n")

with open('ALL_182_KEYWORDS.txt','w') as f:
    f.write("ALL 182 CAREER KEYWORDS\n"+"="*60+"\n\n")
    for i, row in df.iterrows(): f.write(f"{i+1:3d}. {row.career}\n\n")

# Combined PDF files
pdf = FPDF(); pdf.add_page(); pdf.set_font('Arial','B',18)
pdf.cell(0,15,'ALL 182 STATEMENTS',0,1,'C'); pdf.ln(10)
pdf.set_font('Arial','',10)
for i, row in df.iterrows():
    if (i+1)%20==1 and i>0: pdf.add_page()
    pdf.cell(0,5,f"{i+1:3d}.",0,1); pdf.multi_cell(0,4,row.statement); pdf.ln(2)
pdf.output('ALL_182_STATEMENTS.pdf')

pdf = FPDF(); pdf.add_page(); pdf.set_font('Arial','B',18)
pdf.cell(0,15,'ALL 182 KEYWORDS',0,1,'C'); pdf.ln(10)
pdf.set_font('Arial','',12)
for i, row in df.iterrows():
    if (i+1)%25==1 and i>0: pdf.add_page()
    pdf.cell(0,8,f"{i+1:3d}. {row.career}",0,1)
pdf.output('ALL_182_KEYWORDS.pdf')

# ZIP individual files
with zipfile.ZipFile('182_INDIVIDUAL_FILES.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir('individual'): z.write(f'individual/{f}',f)

# DOWNLOAD ALL 6 FILES
print("\n DOWNLOADING 6 PERFECT FILES...")
files.download('182_INDIVIDUAL_FILES.zip')  # 364 files
files.download('ALL_182_STATEMENTS.txt')
files.download('ALL_182_KEYWORDS.txt')
files.download('ALL_182_STATEMENTS.pdf')
files.download('ALL_182_KEYWORDS.pdf')

print("\n🎉  ALL 3 BLOCKS COMPLETE!")
print("🔧 FIXED: Keywords now show COMPLETE CAREER TITLES (no random words/names)")
print(" 182_INDIVIDUAL_FILES.zip  ← 364 files (182 txt + 182 pdf)")
print(" ALL_182_STATEMENTS.txt    ← All statements")
print(" ALL_182_KEYWORDS.txt      ← All keywords")
print(" ALL_182_STATEMENTS.pdf    ← All statements")
print(" ALL_182_KEYWORDS.pdf      ← All keywords")
