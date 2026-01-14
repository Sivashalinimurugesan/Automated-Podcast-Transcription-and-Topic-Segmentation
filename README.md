## Automated Podcast Transcription & Topic Segmentation

This project implements an AI-powered pipeline to automatically transcribe podcast audio files, segment long transcripts into meaningful sections, extract keywords, and generate initial summaries.

It is designed to help users efficiently navigate and analyze long-form audio content such as podcasts, interviews, and lectures.

------------------------------------------------------------------------

## 1. Project Overview

 Podcasts often span several hours, making it difficult to locate specific discussions or topics.
 This system solves that problem by:

 * Converting audio into accurate text transcripts

 * Structuring transcripts into smaller semantic segments

 * Extracting representative keywords for each segment

 * Generating initial summaries for quick understanding

 * The project focuses on speed, modularity, and explainability, making it suitable for academic, internship, and production-oriented workflows.

## Objectives

 * Transcribe podcast audio using fast and accurate speech-to-text models

 * Preprocess and normalize audio for better transcription quality

 * Segment transcripts into manageable, topic-oriented chunks

 * Extract keywords for each segment to support topic discovery

 * Generate initial summaries to provide high-level context

 * Maintain a clean, modular, and extensible pipeline

------------------------------------------------------------------------

## 2. Project Structure

```text
Automated-Podcast-Transcription-and-Topic-Segmentation/
│
├── audio_raw/               # Storage for original uploaded audio files
├── audio_processed/         # Cleaned and normalized audio (WAV format)
├── transcripts/             # Transcribed files saved as .txt
├── segments/                # Segments of each transcript saved as JSON
├── keywords/                # Keywords extracted for segments
├── summaries/               # Summaries of transcripts
│
├── src/                     # Main source code modules
│   ├── preprocessing.py     # Audio cleaning, VAD, and normalization
│   ├── transcription.py     # Whisper AI speech-to-text pipeline
│   ├── segmentation.py      # Topic segmentation logic
│   ├── summarization.py     # Text summarization
│   └── keyword_extraction.py # Keyword extraction

 ```

------------------------------------------------------------------------

## 3. Technology Stack

 Programming Language
  * Python 3.12

 Speech-to-Text
   * Faster-Whisper – Optimized Whisper inference using CTranslate2
   * GPU support (optional)

 Audio Processing
   * SoundFile
   * Librosa
  NumPy

 Natural Language Processing
  * NLTK – Sentence tokenization
  * Scikit-learn
   * TF-IDF vectorization
   * Cosine similarity

 Data Handling
  * JSON
  * OS / Glob utilities
 Visualization and UI
  * Streamlit: Interactive web dashboard creation.
 
------------------------------------------------------------------------

## 4. Workflow

 1) Audio Ingestion
   *  Place raw podcast audio files into audio_raw/

 2) Audio Preprocessing
    * Noise handling
    * Normalization
    * Conversion to WAV format
  Output → audio_preprocessed/

 3) Transcription
    * Fast speech-to-text using Faster-Whisper
    * One transcript per audio file
  Output → transcripts/

 4) Segmentation
    * Sentence-based segmentation
    * Fixed-size semantic chunks
  Output → segmented_transcripts/

 5) Keyword Extraction
    * TF-IDF + diversity-aware selection (MMR)
    * Prevents repeated keywords across segments
  Output → keywords/

6) Initial Summarization
   * Extractive summarization using TF-IDF
   * Produces a high-level overview of each transcript
 Output → summaries/

------------------------------------------------------------------------

## 5. System Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/springboardmentor13579x-proj/Automated-Podcast-Transcription-and-Topic-Segmentation.git
cd Automated-Podcast-Transcription-and-Topic-Segmentation
git checkout intern-bhaskar
```

### Step 2: Create Virtual Environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Execute the Backend Pipeline

```bash
python -m src.main
```

### Step 5: Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

------------------------------------------------------------------------

## 6. Usage

 * Place TED Talk or podcast audio files (.wav, .mp3, .m4a) in the audio_raw/ directory or upload them through the Streamlit interface.

 * Run the backend pipeline or Streamlit app to preprocess audio, generate transcripts, and segment long talks into topic-based sections.

 * Explore each segment using extracted keywords to quickly locate relevant parts of long TED Talks or lectures.

 * View initial summaries and sentiment insights to gain a high-level understanding without reading the full transcript.

 * Use the dashboard for interactive analysis and exploration rather than real-time processing.

------------------------------------------------------------------------

## 7. Limitations & Challenges
 * Transcription accuracy depends heavily on audio quality; noisy or accented speech may reduce performance.

 * Large Whisper models require significant memory, which can be challenging on low-resource systems.

 * Topic segmentation is heuristic-based and may not always perfectly align with true conversational shifts.

 * Keyword extraction and summarization rely on statistical methods and may miss deeper semantic meaning.

 * The system is optimized for offline analysis of datasets like TED Talks, not large-scale real-time deployment.

------------------------------------------------------------------------

## 8. Testing
 * The project includes an automated testing suite to ensure reliability.
 Running Tests:
 ```bash
 python -m pytest
 ```
