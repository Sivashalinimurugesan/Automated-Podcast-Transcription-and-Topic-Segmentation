#  BLOCK 2: GENERATE 182 STATEMENTS + FIXED KEYWORDS + INDIVIDUAL FILES
print(" BLOCK 2: GENERATING DATA + INDIVIDUAL FILES...")

n = 182
careers = ['Machine Learning Engineer','Data Scientist','Software Engineer','Web Developer',
           'Cybersecurity Analyst','Cloud Architect','Mobile Developer','Game Developer',
           'Database Admin','DevOps Engineer']
domains = ['AI/ML','Data Science','Web Dev','Software Eng','Cybersecurity','Cloud Computing',
           'Mobile Dev','Game Dev','Database','DevOps']

def gen_list(base, n): return (base*((n//len(base))+1))[:n]

df = pd.DataFrame({
    'id': range(1,n+1), 'name': [f"Student_{i}" for i in range(1,n+1)],
    'domain': gen_list(domains,n),
    'project': gen_list(['ML Model','Data Analysis','Web App','Software','Security',
                        'Cloud Deploy','Mobile App','Game','DB Design','CI/CD'],n),
    'career': gen_list(careers,n),
    'skills': gen_list(['python strong, sql strong, java average'],n)
})

#  FIXED KEYWORD EXTRACTION - Only future careers, no random words/names
def extract_career_keyword(text):
    text = text.lower()

    # Priority 1: Exact career phrase matches (most reliable)
    career_phrases = {
        'machine learning engineer': 'Machine Learning Engineer',
        'data scientist': 'Data Scientist',
        'software engineer': 'Software Engineer',
        'web developer': 'Web Developer',
        'cybersecurity analyst': 'Cybersecurity Analyst',
        'cloud architect': 'Cloud Architect',
        'mobile developer': 'Mobile Developer',
        'game developer': 'Game Developer',
        'database admin': 'Database Admin',
        'devops engineer': 'DevOps Engineer',
        'full stack developer': 'Software Engineer',
        'data analyst': 'Data Scientist',
        'backend developer': 'Software Engineer',
        'frontend developer': 'Web Developer'
    }

    words = re.sub(r'[^a-z\s]','',text).split()
    word_set = set(words)

    for phrase, career in career_phrases.items():
        if all(word in word_set for word in phrase.split()):
            return career

    # Priority 2: Single career words if no full phrase found
    career_words = ['ml', 'ai', 'data', 'web', 'cyber', 'cloud', 'mobile', 'game', 'database', 'devops']
    tech_count = Counter(w for w in words if w in career_words and len(w)>2)
    if tech_count:
        top_tech = tech_count.most_common(1)[0][0]
        mapping = {'ml':'Machine Learning Engineer', 'ai':'Machine Learning Engineer',
                  'data':'Data Scientist', 'web':'Web Developer', 'cyber':'Cybersecurity Analyst',
                  'cloud':'Cloud Architect', 'mobile':'Mobile Developer', 'game':'Game Developer',
                  'database':'Database Admin', 'devops':'DevOps Engineer'}
        return mapping.get(top_tech, 'Software Engineer')

    return 'Software Engineer'  # Default fallback

# Extract REAL career keywords from transcripts (if available)
if summarized_transcripts:
    real_careers = []
    for v in summarized_transcripts.values():
        career = extract_career_keyword(v['original'])
        real_careers.append(career)
    df['career'] = real_careers[:n]
    print(f" Extracted {len(real_careers)} REAL CAREER KEYWORDS from transcripts")
else:
    print(" Using predefined career list")

df['statement'] = df.apply(lambda r:
    f"if you are interested in {r.domain.lower()} and they have worked on {r.project.lower()}. "
    f"skills levels are {r.skills}. The suggested future career is {r.career}", axis=1)

os.makedirs('individual', exist_ok=True)
for i, row in tqdm(df.iterrows(), total=n, desc="Individual files"):
    sid = f"s{i+1:03d}"

    # TXT files
    with open(f'individual/{sid}_statement.txt','w') as f: f.write(row.statement)
    with open(f'individual/{sid}_keyword.txt','w') as f: f.write(row.career)

    # Statement PDF
    pdf = FPDF(); pdf.add_page()
    pdf.set_font('Arial','B',16); pdf.cell(0,10,f"Student {i+1}",0,1,'C')
    pdf.ln(5); pdf.set_font('Arial','',12); pdf.multi_cell(0,6,row.statement)
    pdf.output(f'individual/{sid}_statement.pdf')

    # FIXED Keyword PDF - FULL CAREER TEXT, NO CUT-OFF
    pdf = FPDF(); pdf.add_page()
    pdf.set_font('Arial','B',28); pdf.set_text_color(102,126,234)  # Reduced from 32
    pdf.cell(0,60,row.career,0,1,'C')  # Increased vertical space
    pdf.ln(20); pdf.set_font('Arial','',14); pdf.set_text_color(0,0,0)
    pdf.cell(0,10,f"Student {i+1:03d}: {row.name}",0,1,'C')
    pdf.output(f'individual/{sid}_keyword.pdf')

print(" BLOCK 2 COMPLETE! Keywords now show FULL CAREER TITLES!")
