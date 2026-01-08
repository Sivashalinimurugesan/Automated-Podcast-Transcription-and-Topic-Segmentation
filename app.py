import streamlit as st 
import os, json, re, logging
from sklearn.feature_extraction.text import TfidfVectorizer
from pydub import AudioSegment
import matplotlib.pyplot as plt
from io import BytesIO
from collections import Counter
import whisper
import nltk
from wordcloud import WordCloud


# -----------------------------
# NLTK Offline Setup
# -----------------------------
nltk.data.path.append(r"C:\Users\USER\nltk_data")
from nltk.tokenize import sent_tokenize

# -----------------------------
# CONFIG PATHS
# -----------------------------
from config import AUDIO_PROCESSED_DIR as AUDIO_DIR, WHISPER_MODEL, MIN_MEDICAL_TERMS

# Save JSON in your existing folder
JSON_DIR = r"C:\Users\USER\OneDrive\Desktop\Project\segments_KeywordExtract_Summary"
import os
os.makedirs(JSON_DIR, exist_ok=True)

import os, logging

# Make sure directories exist
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# Define LOG_DIR relative to AUDIO_DIR
LOG_DIR = os.path.join(os.path.dirname(AUDIO_DIR), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# -----------------------------
# LOGGING SETUP
# -----------------------------
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Application started")

# -----------------------------
# HELPERS
# -----------------------------

import shutil

from config import AUDIO_RAW_DIR, AUDIO_PROCESSED_DIR, SEGMENTS_DIR


def sync_raw_to_processed():
    """
    Ensures audio_processed contains all audios
    that already have JSON segments.
    """
    for jf in os.listdir(SEGMENTS_DIR):
        if not jf.endswith("_segments.json"):
            continue

        base = jf.replace("_segments.json", "")

        for ext in (".mp3", ".wav"):
            src = os.path.join(AUDIO_RAW_DIR, base + ext)
            dst = os.path.join(AUDIO_PROCESSED_DIR, base + ext)

            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)

def sec_to_mmss(sec):
    m, s = divmod(int(sec), 60)
    return f"{m:02d}:{s:02d}"

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()

def segment_text(text, size=5):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i+size]) for i in range(0, len(sentences), size)]

def extract_keywords(text, k=5):
    try:
        v = TfidfVectorizer(stop_words="english")
        x = v.fit_transform([text])
        scores = x.toarray()[0]
        words = v.get_feature_names_out()
        return [words[i] for i in scores.argsort()[-k:][::-1]]
    except Exception as e:
        logging.error(f"Keyword extraction failed: {e}")
        return []

def summarize_text(text, n=2):
    sents = sent_tokenize(text)
    if len(sents) <= n:
        return text
    try:
        v = TfidfVectorizer(stop_words="english")
        x = v.fit_transform(sents)
        scores = x.sum(axis=1).A1
        idx = sorted(scores.argsort()[-n:])
        return " ".join(sents[i] for i in idx)
    except Exception as e:
        logging.error(f"Summary failed: {e}")
        return "Summary unavailable."

def process_transcript(text, duration):
    chunks = segment_text(text)
    if not chunks:
        logging.warning("No transcript chunks generated")
        return []

    sec = duration / len(chunks)
    segments = []

    for i, chunk in enumerate(chunks, 1):
        segments.append({
            "segment_id": i,
            "start_time": (i - 1) * sec,
            "end_time": i * sec,
            "text": chunk,
            "keywords": extract_keywords(chunk),
            "summary": summarize_text(chunk)
        })

    logging.info(f"Created {len(segments)} segments")
    return segments

def save_segments_json(segments, name):
    path = os.path.join(JSON_DIR, f"{name}_segments.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

def extract_top_medical_words(segments, top_n=15):
    # Combine transcript of selected audio
    text = " ".join(s["text"] for s in segments).lower()

    # Extract clean words
    words = re.findall(r"\b[a-z]{3,}\b", text)

    # Remove English stopwords
    stopwords = set(TfidfVectorizer(stop_words="english").get_stop_words())

    # Keep only medical terms
    medical_words = [
        w for w in words
        if w not in stopwords and w in MEDICAL_TERMS
    ]

    return Counter(medical_words).most_common(top_n)

        # -----------------------------
# MEDICAL SENTIMENT ANALYSIS
# -----------------------------
MEDICAL_POSITIVE = {
    "improve", "improvement", "improving",
    "recovery", "recover", "recovered",
    "effective", "efficacy", "successful", "success",
    "stable", "stabilized", "normal", "normalized",
    "safe", "safer", "safely",
    "benefit", "beneficial",
    "controlled", "under control",
    "relief", "relieved", "relieving",
    "healed", "healing", "cured", "curable",
    "responsive", "responding", "response",
    "reduced", "reduction", "lowered",
    "improved outcome", "favorable", "promising",
    "well tolerated", "tolerated",
    "managed", "manageable",
    "resolution", "resolved",
    "asymptomatic", "remission",
    "good prognosis", "positive outcome"
}

MEDICAL_NEGATIVE = {
    "pain", "painful", "severe pain",
    "risk", "risky", "high risk",
    "infection", "infected", "infectious",
    "failure", "failed", "nonresponsive",
    "severe", "critical", "life-threatening",
    "complication", "complications",
    "worsen", "worsening", "deterioration",
    "death", "fatal", "mortality",
    "disease progression", "progressive",
    "bleeding", "hemorrhage",
    "toxic", "toxicity", "adverse",
    "side effects", "adverse effects",
    "hospitalized", "icu", "intensive care",
    "chronic", "incurable",
    "malignant", "metastasis",
    "relapse", "recurrence",
    "uncontrolled", "unstable",
    "poor prognosis", "negative outcome"
}
MEDICAL_TERMS = {

    # ---------------- Patients & Care ----------------
    "patient", "patients", "case", "cases",
    "outpatient", "inpatient", "admission", "discharge",
    "care", "healthcare", "medical", "clinical",
    "followup", "consultation", "referral", "triage",

    # ---------------- Diagnosis & Conditions ----------------
    "diagnosis", "diagnostic", "condition", "conditions",
    "disease", "disorder", "syndrome", "illness", "pathology",
    "infection", "infections", "viral", "bacterial", "fungal",
    "acute", "chronic", "congenital", "autoimmune",
    "idiopathic", "inflammatory", "degenerative",
    "hereditary", "genetic",

    # ---------------- Symptoms & Signs ----------------
    "symptom", "symptoms", "sign", "signs",
    "pain", "fever", "fatigue", "weakness",
    "nausea", "vomiting", "diarrhea", "constipation",
    "headache", "dizziness", "vertigo",
    "cough", "breathlessness", "dyspnea",
    "chestpain", "palpitations",
    "inflammation", "swelling", "edema",
    "bleeding", "hemorrhage", "bruising",
    "rash", "lesion",

    # ---------------- Medications & Treatment ----------------
    "treatment", "therapy", "therapies",
    "medication", "medications", "pharmacotherapy",
    "drug", "drugs", "antibiotic", "antibiotics",
    "antiviral", "antifungal", "antipyretic",
    "analgesic", "anesthetic", "steroid", "corticosteroid",
    "chemotherapy", "radiotherapy", "immunotherapy",
    "dose", "dosage", "prescription", "regimen",
    "vaccine", "vaccination", "immunization",
    "prophylaxis", "infusion", "injection",
    "compliance", "adherence",

    # ---------------- Tests & Procedures ----------------
    "test", "tests", "screening", "biopsy", "scan",
    "imaging", "radiology",
    "xray", "ct", "mri", "pet", "ultrasound",
    "ecg", "ekg", "eeg", "echo",
    "blood", "urine", "stool", "sample", "specimen",
    "lab", "laboratory", "culture", "assay",
    "report", "results", "findings",

    # ---------------- Hospitals & Facilities ----------------
    "hospital", "clinic", "ward", "icu", "nicu",
    "emergency", "er", "trauma",
    "surgery", "surgical", "procedure", "operation",
    "anesthesia", "postoperative", "preoperative",
    "recoveryroom",

    # ---------------- Body Systems ----------------
    "heart", "cardiac", "cardiovascular",
    "lungs", "pulmonary", "respiratory",
    "brain", "neurological", "nervous",
    "kidney", "renal", "urinary",
    "liver", "hepatic",
    "gastrointestinal", "digestive",
    "endocrine", "hormonal",
    "musculoskeletal", "skeletal",
    "immune", "immunological",

    # ---------------- Diseases (Expanded) ----------------
    "cancer", "tumor", "neoplasm", "malignancy",
    "diabetes", "hypertension", "hypotension",
    "asthma", "copd", "bronchitis",
    "arthritis", "osteoarthritis", "rheumatoid",
    "stroke", "sepsis", "shock",
    "covid", "tuberculosis", "pneumonia",
    "influenza", "hepatitis", "hiv",
    "obesity", "anemia", "thrombosis",

    # ---------------- Risk, Complications & Outcomes ----------------
    "risk", "riskfactor", "complication", "complications",
    "sideeffect", "sideeffects", "adverse",
    "toxicity", "mortality", "morbidity",
    "recovery", "improvement", "deterioration",
    "prognosis", "relapse", "recurrence",
    "remission", "outcome", "survival",

    # ---------------- Medical Staff ----------------
    "doctor", "physician", "surgeon", "nurse",
    "paramedic", "therapist", "radiologist",
    "pathologist", "anesthesiologist",
    "specialist", "consultant",

    # ---------------- Public Health & Research ----------------
    "epidemiology", "prevalence", "incidence",
    "clinicaltrial", "randomized", "cohort",
    "study", "research", "analysis",
    "guideline", "protocol", "evidence",
    "screeningprogram", "surveillance",

}

# -----------------------------
# KEYWORD CLOUD CONFIG
# -----------------------------
MIN_MEDICAL_TERMS = 5




def medical_sentiment(text):
    text = text.lower()
    pos = sum(word in text for word in MEDICAL_POSITIVE)
    neg = sum(word in text for word in MEDICAL_NEGATIVE)

    if pos > neg:
        return "Positive"
    elif neg > pos:
        return "Negative"
    else:
        return "Neutral"

def sentiment_distribution(segments):
    sentiments = [medical_sentiment(s["text"]) for s in segments]
    return Counter(sentiments)


# -----------------------------
# WHISPER SAFE
# -----------------------------
@st.cache_resource
def load_whisper():
    logging.info("Loading Whisper model")
    return whisper.load_model("base")

def transcribe_audio_safe(audio_path):
    try:
        model = load_whisper()

        if os.path.getsize(audio_path) < 1000:
            logging.warning("Audio file too small")
            return ""

        result = model.transcribe(
            audio_path,
            fp16=False,
            condition_on_previous_text=False
        )

        return result.get("text", "").strip()

    except Exception as e:
        logging.error(f"Whisper failed: {e}")
        return ""

# -----------------------------
# GLOBAL SEARCH
# -----------------------------
def global_search(query):
    results = []

    for jf in os.listdir(JSON_DIR):
        if not jf.endswith("_segments.json"):
            continue

        audio_name = jf.replace("_segments.json", "")
        with open(os.path.join(JSON_DIR, jf), encoding="utf-8") as f:
            segments = json.load(f)

        for seg in segments:
            if query.lower() in seg["text"].lower():
                results.append({
                    "audio": audio_name,
                    "segment_id": seg["segment_id"],
                    "start": seg["start_time"],
                    "end": seg["end_time"],
                    "text": seg["text"]
                })

    return results

def highlight(text, query):
    return re.sub(
        f"({re.escape(query)})",
        r"<span style='background-color:#d63031;color:white;padding:2px 6px;border-radius:5px;'>\1</span>",
        text,
        flags=re.IGNORECASE
    )

# -----------------------------
# STREAMLIT APP
# -----------------------------
def main():
   
    sync_raw_to_processed()
    
    st.set_page_config(
        page_title="Transcript Navigator",
        layout="wide"
    )
   
    

    st.markdown("""
    <style>
    /* General App */
    .stApp {
        background-color:#0e0e0e;
        color:#f5f6fa;
        font-family: 'Segoe UI', sans-serif;
    }
    h1,h2,h3,h4,h5,h6 { color:#ffd700; font-weight:700; }

    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #f12711, #f5af19);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 8px 16px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(255,255,255,0.3);
    }

    /* Keyword tags */
    .keyword {
        display:inline-block;
        background: #00a8cc;
        color:white;
        padding:5px 14px;
        border-radius:25px;
        margin:3px 4px;
        font-weight:bold;
    }

    /* Summary box */
    .summary-box {
        background:#1b262c;
        color:white;
        border-left:6px solid #00cec9;
        padding:16px;
        border-radius:12px;
        margin-bottom:12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        max-height: 300px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    /* Transcript box */
    .transcript-box {
        background:#2d3436;
        color:#f5f6fa;
        border-left:6px solid #fdcb6e;
        padding:16px;
        border-radius:12px;
        margin-bottom:12px;
        line-height:1.6;
        font-size:16px;
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    /* Audio player styling */
    audio { width: 100%; margin: 12px 0; }

    /* Tab headers */
    div.stTabs [role="tab"] {
        background: #ff416c;
        color:white;
        font-weight:bold;
        border-radius:10px 10px 0 0;
        padding:8px 12px;
    }
    div.stTabs [role="tab"]:hover { background: #ff758c; color:white; }
    </style>
    """, unsafe_allow_html=True)

    st.title(" Transcript Navigation & Global Search")
    tab1, tab2, tab3, tab4 = st.tabs([
    "Audio Navigator",
    "Global Transcript Search",
    "Sentiment Analysis",
    "Keyword Cloud"  # <-- new TAB 4
])

    # ---------------- TAB 1 ----------------
    with tab1:
        uploaded_audio = st.file_uploader("Upload audio", type=["mp3", "wav"])
        audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith((".mp3", ".wav"))]

        audio_path = None
        if uploaded_audio:
            audio_path = os.path.join(AUDIO_DIR, uploaded_audio.name)
            with open(audio_path, "wb") as f:
                f.write(uploaded_audio.read())
        elif audio_files:
            audio_path = os.path.join(AUDIO_DIR, st.selectbox("Select audio", audio_files))
        else:
            st.info("Upload or add audio files")
            return

        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        json_path = os.path.join(JSON_DIR, f"{base_name}_segments.json")

        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000

        if os.path.exists(json_path):
            with open(json_path, encoding="utf-8") as f:
                segments = json.load(f)
        else:
            text = clean_text(transcribe_audio_safe(audio_path))
            segments = process_transcript(text, duration)
            save_segments_json(segments, base_name)

        st.audio(open(audio_path, "rb").read())

        keywords = sorted({k for s in segments for k in s["keywords"]})
        selected_kw = st.selectbox("Filter by keyword", ["All"] + keywords)
        search_query = st.text_input("Search in transcript")

        filtered = [
            s for s in segments
            if (selected_kw == "All" or selected_kw in s["keywords"])
            and (not search_query or search_query.lower() in s["text"].lower())
        ]

        col1, col2 = st.columns([1, 2])
        with col1:
            for seg in filtered:
                if st.button(
                    f"Segment {seg['segment_id']}  {sec_to_mmss(seg['start_time'])}",
                    key=f"seg{seg['segment_id']}"
                ):
                    st.session_state.current_segment = seg
                    st.rerun()

        with col2:
            if "current_segment" in st.session_state:
                seg = st.session_state.current_segment
                st.markdown("###  Keywords")
                st.markdown(
                    "".join(f"<span class='keyword'>{k}</span>" for k in seg["keywords"]),
                    unsafe_allow_html=True
                )
                st.markdown("### Summary")
                st.markdown(f"<div class='summary-box'>{seg['summary']}</div>", unsafe_allow_html=True)
                st.markdown("###  Transcript")
                st.markdown(f"<div class='transcript-box'>{seg['text']}</div>", unsafe_allow_html=True)
            else:
                st.info("Select a segment")

    # ---------------- TAB 2 ----------------
    with tab2:
        query = st.text_input("Search across all transcripts")
        if query:
            results = global_search(query)
            if not results:
                st.warning("No matches found")
            else:
                for r in results:
                    st.markdown("---")
                    st.markdown(f"###  Audio: **{r['audio']}**")
                    st.markdown(f" **Segment Time:** {sec_to_mmss(r['start'])} → {sec_to_mmss(r['end'])}")
                    st.markdown(f"<div class='transcript-box'><b>Segment #{r['segment_id']}</b><br><br>{highlight(r['text'], query)}</div>", unsafe_allow_html=True)
                    for f in os.listdir(AUDIO_DIR):
                        if r["audio"].lower() in f.lower():
                            st.audio(open(os.path.join(AUDIO_DIR, f), "rb").read())
                            break


                        
        
        # ---------------- TAB 3 ----------------
    with tab3:
        st.subheader(f"Medical Podcast Sentiment Analysis for: {base_name}")

        if not segments:
            st.info("Please load an audio file to view sentiment analysis.")
        else:
            # Calculate sentiment for each segment
            sentiments = [medical_sentiment(s["text"]) for s in segments]
            sentiment_counts = Counter(sentiments)
            total_segments = len(segments)

            labels = ["Positive", "Neutral", "Negative"]
            rates = [
                round((sentiment_counts.get(label, 0) / total_segments) * 100, 2)
                for label in labels
            ]
            x_positions = range(len(labels))

            # Create point graph
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.scatter(x_positions, rates, s=10)
            ax.set_xticks(x_positions)
            ax.set_xticklabels(labels)
            ax.set_xlabel("Sentiment Type")
            ax.set_ylabel("Rate (%)")
            ax.set_ylim(0, 100)
            ax.set_title(f"Sentiment Rate for Audio File: {base_name}", fontsize=7)

            # Add value labels
            for x, y in zip(x_positions, rates):
                ax.text(x, y + 2, f"{y}%", ha="center", fontsize=4, fontweight="bold")
            plt.tight_layout()

            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)

            # -----------------------------
            # Layout: Left = Explanation + Indexed Segments | Right = Graph
            # -----------------------------
            left_col, right_col = st.columns([2, 1])

            # LEFT: How to read graph + Segment-wise sentiment
            with left_col:
                st.markdown("### How to read this graph")
                st.markdown("""
                - Each **dot** represents the percentage of sentiment across podcast segments  
                - **Higher point → More dominant sentiment**
                """)
                st.markdown("**Sentiment Meaning**")
                st.markdown("- 1. **Positive** → Recovery, improvement, effective treatment")
                st.markdown("- 2. **Neutral** → Informational medical discussion")
                st.markdown("- 3. **Negative** → Risk, complications, or critical conditions")
                st.markdown("---")

                st.markdown("###  Segment-wise Sentiment")
                for i, s in enumerate(segments, 1):
                    seg_sentiment = medical_sentiment(s["text"])
                    st.markdown(f"**Segment #{i}** | Sentiment: **{seg_sentiment}**")
                    st.markdown(f"{s['text']}")
                    st.markdown("---")

            # RIGHT: Sentiment graph
            with right_col:
                st.pyplot(fig)  # directly displays the Matplotlib figure

                # ---------------- TAB 4 ----------------
    # ---------------- TAB 4 ----------------
    with tab4:
        st.subheader(f"Keyword Analysis for: {base_name}")

        if not segments:
            st.info("Please load an audio file to see keyword analysis.")
        else:
        # --------------------------------------------------
        # 1. Combine text
        # --------------------------------------------------
            full_text = " ".join(s["text"] for s in segments).lower()

        # --------------------------------------------------
        # 2. Clean words
        # --------------------------------------------------
            words = re.findall(r"\b[a-z]{3,}\b", full_text)
            stopwords = set(TfidfVectorizer(stop_words="english").get_stop_words())
            words = [w for w in words if w not in stopwords]

        # --------------------------------------------------
        # 3. Medical filtering
        # --------------------------------------------------
        medical_words = [w for w in words if w in MEDICAL_TERMS]
        medical_freq = Counter(medical_words)

        if len(medical_freq) >= MIN_MEDICAL_TERMS:
            final_freq = dict(medical_freq.most_common(10))
        else:
            final_freq = dict(Counter(words).most_common(10))

        if not final_freq:
            st.warning("No keywords found.")
        else:
            # --------------------------------------------------
            # 4. Summary metrics
            # --------------------------------------------------
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Keywords", len(final_freq))
            m2.metric("Top Keyword", max(final_freq, key=final_freq.get))
            m3.metric("Highest Frequency", max(final_freq.values()))

            # --------------------------------------------------
            # 5. Layout: LEFT = Frequency | RIGHT = Cloud
            # --------------------------------------------------
            left_col, right_col = st.columns(2)

            # ================= LEFT: KEYWORD FREQUENCY =================
            with left_col:
                st.markdown("###  Keyword Frequency")

                keywords = list(final_freq.keys())
                frequencies = list(final_freq.values())

                fig_bar, ax_bar = plt.subplots(figsize=(7, 4))
                bars = ax_bar.barh(keywords, frequencies)

                ax_bar.set_xlabel("Number of Times Mentioned")
                ax_bar.set_ylabel("Keywords")

                # Clean look
                ax_bar.spines["top"].set_visible(False)
                ax_bar.spines["right"].set_visible(False)

                max_val = max(frequencies)
                ax_bar.set_xlim(0, max_val * 1.15)

                # Numbers beside bars
                for bar in bars:
                    value = int(bar.get_width())
                    ax_bar.text(
                        value + max_val * 0.02,
                        bar.get_y() + bar.get_height() / 2,
                        str(value),
                        va="center",
                        fontsize=11,
                        fontweight="bold"
                    )

                st.pyplot(fig_bar)

            # ================= RIGHT: KEYWORD CLOUD =================
            with right_col:
                st.markdown("###  Keyword Cloud")

                wc = WordCloud(
                    width=600,
                    height=400,
                    background_color="white",
                    colormap="plasma"
                ).generate_from_frequencies(final_freq)

                fig_wc, ax_wc = plt.subplots(figsize=(7, 4))
                ax_wc.imshow(wc, interpolation="bilinear")
                ax_wc.axis("off")

                st.pyplot(fig_wc)

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()