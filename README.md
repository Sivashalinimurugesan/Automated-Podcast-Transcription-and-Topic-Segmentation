# Automated Podcast Transcription and Topic Segmentation

## An AI-Based System for HR Interviews, Corporate Meetings, and Spoken Content Analysis

------------------------------------------------------------------------

## 1. Overview

The **Automated Podcast Transcription and Topic Segmentation** project
presents an end-to-end artificial intelligence system for processing
long-form spoken content such as **HR interviews, corporate meetings,
podcasts, webinars, and lectures**. The system automatically converts
audio into text, identifies topic boundaries, segments conversations
into coherent sections, and generates summaries and keywords for each
segment.

The primary motivation of this work is to support **organizational
communication analysis**, with a particular emphasis on **human resource
(HR) interviews and business meetings**, where efficient navigation,
summarization, and evaluation of spoken content are essential. By
integrating speech recognition, natural language processing (NLP), and
machine learning techniques, the system enables structured analysis of
otherwise unstructured audio data.

------------------------------------------------------------------------

## 2. Methodological Approach

The system is designed as a modular pipeline, enabling independent
development and evaluation of each processing stage:

    Audio Input → Preprocessing → ASR Transcription → Topic Segmentation
                       ↓
              Summarization & Keyword Extraction
                       ↓
               Evaluation and Visualization / UI

### 2.1 Audio Preprocessing

-   Converts audio into a standardized format and sampling rate\
-   Reduces background noise and normalizes amplitude levels\
-   Ensures consistent input quality for downstream ASR models

### 2.2 Automatic Speech Recognition (ASR)

-   Employs OpenAI Whisper to convert audio into textual transcripts\
-   Supports conversational speech typical of interviews and meetings

### 2.3 Topic Segmentation

-   Identifies topic shifts using text similarity and structural cues\
-   Divides transcripts into meaningful segments corresponding to
    discussion themes

### 2.4 Summarization

-   Generates concise segment-level summaries\
-   Removes filler tokens, non-informative markers, and segmentation
    artifacts

### 2.5 Keyword Extraction

-   Uses TF--IDF with uni-grams and bi-grams\
-   Extracts representative terms without redundancy

### 2.6 Transcription Evaluation

-   Compares ASR outputs with reference transcripts\
-   Computes:
    -   Word Error Rate (WER)\
    -   Character Error Rate (CER)\
    -   Overall transcription accuracy

------------------------------------------------------------------------

## 3. Technology Stack

### Core Technologies

-   Python 3.9+\
-   OpenAI Whisper (Automatic Speech Recognition)\
-   Librosa, FFmpeg, PyDub (audio processing)

### Natural Language Processing

-   NLTK\
-   Scikit-learn\
-   HuggingFace Transformers\
-   Sentence Transformers (optional)

### Visualization and Interface

-   Streamlit\
-   Plotly / Matplotlib\
-   WordCloud

### Evaluation and Storage

-   jiwer (ASR evaluation metrics)\
-   CSV and TXT formats for intermediate and final outputs

------------------------------------------------------------------------

## 4. System Setup

### Step 1: Clone the Repository

``` bash
git clone https://github.com/springboardmentor13579x-proj/Automated-Podcast-Transcription-and-Topic-Segmentation.git
cd Automated-Podcast-Transcription-and-Topic-Segmentation
```

### Step 2: Create Virtual Environment (Optional)

``` bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### Step 3: Install Dependencies

``` bash
pip install -r requirements.txt
```

### Step 4: Execute the Pipeline

``` bash
python -m src.main
```

------------------------------------------------------------------------

## 5. Directory Structure

    project/
    │── audio_raw/
    │── audio_processed/
    │── transcripts/
    │   ├── asr/
    │   ├── raw_reference/
    │   └── final/
    │── segments/
    │── src/
    │   ├── preprocessing.py
    │   ├── transcription.py
    │   ├── segmentation.py
    │   ├── summarization.py
    │   ├── keyword_extraction.py
    │   ├── evaluate_asr.py
    │   ├── ui_app.py
    │   └── main.py
    │── docs/
    │── results/
    │── README.md
    │── requirements.txt
    │── LICENSE

------------------------------------------------------------------------

## 6. Use Cases

### 6.1 HR Interviews (Primary Application)

The system is designed to support the automated analysis of HR
interviews by: - Generating transcripts of interview sessions\
- Segmenting interviews by topics such as candidate background,
technical discussion, behavioral assessment, and closing remarks\
- Extracting keywords related to skills, experience, and organizational
fit\
- Producing summaries that highlight key evaluation points\
- Enabling structured review of interview content for recruitment and
decision-making

### 6.2 Corporate Meetings

For business and management contexts, the system: - Segments long
meetings by agenda topics\
- Produces executive summaries\
- Tracks discussion outcomes and decisions\
- Facilitates rapid review of meeting proceedings

### 6.3 Podcasts and Webinars

-   Creates topical chapters within long recordings\
-   Enables keyword-based navigation and search\
-   Generates concise content summaries

### 6.4 Academic Lectures

-   Breaks lectures into instructional modules\
-   Extracts important technical concepts\
-   Supports student revision and content indexing

### 6.5 Accessibility

-   Provides text-based access to spoken content for hearing-impaired
    users\
-   Enhances inclusivity in education and organizational communication

------------------------------------------------------------------------

## 7. Troubleshooting

**ASR Not Running Correctly**\
- Ensure Whisper and FFmpeg are installed\
- Verify audio files exist in `audio_raw/`

**Segmentation Produces No Output**\
- Confirm transcripts are present in `transcripts/asr/`\
- Run:

``` bash
python src/segmentation.py
```

**Keyword Repetition or Noise**\
- Check text cleaning functions for segmentation markers and timestamps\
- Ensure TF--IDF parameters are properly configured

**Evaluation Errors**\
- Ensure reference transcripts exist in `transcripts/raw_reference/`\
- File names must exactly match ASR outputs

**Large File Upload Issues**\
- GitHub restricts files larger than 100 MB\
- Use `.gitignore`, Git LFS, or external storage (Google Drive) for raw
audio

------------------------------------------------------------------------

## 8. Limitations and Challenges

-   **Speech Recognition Accuracy:** Performance may degrade for noisy
    audio, overlapping speech, or strong accents.\
-   **Topic Boundary Detection:** Subtle conversational transitions may
    not always be detected.\
-   **Summarization Quality:** Extractive summaries may lack deeper
    semantic abstraction.\
-   **Scalability:** The current pipeline is batch-based and not
    optimized for real-time streaming.\
-   **Data Management:** Large audio files pose challenges for version
    control and repository storage.

------------------------------------------------------------------------

## 9. Future Scope

-   Integration of **multi-speaker diarization** to identify individual
    speakers\
-   **Semantic search** across transcripts using embedding-based
    retrieval\
-   **Sentiment analysis** of interview responses and meeting
    discussions\
-   **Abstractive summarization** using transformer-based models\
-   Full **web deployment** using Streamlit Cloud or similar platforms\
-   **YouTube link ingestion** for automated audio and transcript
    extraction

------------------------------------------------------------------------

## 10. References

1.  Radford, A., et al. (2022). *Robust Speech Recognition via
    Large-Scale Weak Supervision (Whisper).* OpenAI.\
2.  JiWER -- Word Error Rate computation:
    https://github.com/jitsi/jiwer\
3.  Hearst, M. (1997). *TextTiling: Segmenting Text into Multi-Paragraph
    Subtopic Passages.* Computational Linguistics.\
4.  NLTK: https://www.nltk.org/\
5.  HuggingFace Transformers: https://huggingface.co/\
6.  Streamlit: https://streamlit.io/
