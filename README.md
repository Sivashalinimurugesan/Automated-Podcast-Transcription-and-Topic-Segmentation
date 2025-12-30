AUTOMATED PODCAST TRANSCRIPTION AND TOPIC SEGMENTATION

I. Overview

This project provides an end-to-end pipeline to automatically convert meeting or podcast audio into accurate text transcripts, followed by topic-based segmentation, summarization, and keyword extraction using natural language processing techniques. It is designed to efficiently process long-form audio and is suitable for real-world applications such as automated meeting minutes, podcast summarization, and interview analysis.

II. Objectives

Convert audio recordings into accurate text transcripts using OpenAI Whisper.

Segment long conversations into meaningful topics using semantic analysis.

Generate concise summaries for each identified segment.

Extract important keywords for quick understanding of content.

Visualize sentiment and timelines via an interactive dashboard.

III. Key Features

Automatic Speech Recognition (ASR) using OpenAI Whisper for high-accuracy transcription.

Topic Segmentation for long transcripts using TF-IDF and Cosine Similarity.

Summary Generation for segmented content using HuggingFace Transformers (DistilBART).

Keyword Extraction using TF-IDF ranking.

Sentiment Analysis using NLTK VADER to track emotional tone.

Optimized for long meeting and podcast audio.

IV. Dataset

This project was developed and tested using a subset of the TED Talks Audio Dataset.

Source: Kaggle (TED Talks Audio)

Nature: Real-world educational and conversational audio recordings suitable for long-form transcription and topic segmentation tasks.


V. Tech Stack

Python 3.9+

OpenAI Whisper: Speech-to-text

NLTK: Sentence tokenization & Sentiment Analysis

Scikit-learn: TF-IDF Vectorization & Cosine Similarity

HuggingFace Transformers: Summarization (DistilBART)

Streamlit: User Interface

Plotly: Data Visualization


VI. Project Structure

AUTOMATED-PODCAST-TRANSCRIPTION/
│
├── data/                      # Auto-generated Data Storage
│   ├── audio/                 # Raw Input Audio
│   ├── processed_audio/       # 16kHz WAVs
│   ├── transcripts/           # JSON Transcripts with timestamps
│   ├── semantic_segments/     # Topic Segmentation Reports
│   ├── sentiment_data/        # Sentiment scores for graphing
│   ├── short_summary/         # AI Summaries
│   └── keywords/              # Extracted Keywords
│
├── src/                       # Source Code
│   ├── dashboard.py           # Frontend: Streamlit Dashboard UI
│   ├── podcast_backend.py     # Backend: Master AI Logic Pipeline
│   └── __init__.py
│
├── docs/                      # Documentation
│   └── images/                # Screenshots for README
├── tests/                     # Unit Tests
├── .env                       # Environment Variables
├── README.md                  # Project Documentation
├── requirements.txt           # Dependency management
└── LICENSE

* System architecture :
  Audio Input → Preprocessing → Transcription (ASR) → Transcript Cleaning
             ↓
    Embedding Model → Topic Segmentation → Segment Summaries & Keywords
             ↓
          Indexing → UI (Search, Playback, Visualization)
  

VII. How to Run the Project

1. Create and Activate Virtual Environment

Create a virtual environment using:

python -m venv venv


Activate the environment (Windows):

venv\Scripts\activate


2. Install Dependencies

Install all required packages using:

pip install -r requirements.txt


3. Prepare Audio Files

Supported formats: .mp3, .wav, .m4a
Place audio files inside the data/audio/ directory or use the Upload feature in the UI.

4. Run the Application

Execute the main dashboard application:

streamlit run src/dashboard.py


Output files (transcripts, summaries, keywords) will be generated in the data/ directory.

VIII. System Architecture

AUDIO FILES (.MP3 / .WAV)
       ↓
PREPROCESSING (16kHz Mono)
       ↓
OPENAI WHISPER (ASR)
       ↓
TRANSCRIPT FILES (JSON)
       ↓
TOPIC SEGMENTATION (TF-IDF + Cosine Sim)
       ↓
KEYWORD EXTRACTION (TF-IDF)
       ↓
SUMMARY GENERATION (DistilBART)
       ↓
SENTIMENT ANALYSIS (VADER)
       ↓
STRUCTURED OUTPUT & VISUALIZATION


IX. Use Cases

Automated meeting minutes

Podcast summarization

Interview analysis

Research documentation

Content Indexing
