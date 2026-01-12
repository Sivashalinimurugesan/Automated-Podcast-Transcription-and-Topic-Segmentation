🎙️ Automated Podcast Transcription & Topic Segmentation

This project implements an AI-powered pipeline to automatically transcribe podcast audio files, segment long transcripts into meaningful sections, extract keywords, and generate initial summaries.
It is designed to help users efficiently navigate and analyze long-form audio content such as podcasts, interviews, and lectures.

📌 Project Overview

Podcasts often span several hours, making it difficult to locate specific discussions or topics.
This system solves that problem by:

Converting audio into accurate text transcripts

Structuring transcripts into smaller semantic segments

Extracting representative keywords for each segment

Generating initial summaries for quick understanding

The project focuses on speed, modularity, and explainability, making it suitable for academic, internship, and production-oriented workflows.

🎯 Objectives

 Transcribe podcast audio using fast and accurate speech-to-text models

 Preprocess and normalize audio for better transcription quality

 Segment transcripts into manageable, topic-oriented chunks

 Extract keywords for each segment to support topic discovery

 Generate initial summaries to provide high-level context

 Maintain a clean, modular, and extensible pipeline

## 📂 Project Structure

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

🛠️ Technology Stack

Programming Language
 Python 3.12

Speech-to-Text
 Faster-Whisper – Optimized Whisper inference using CTranslate2
  Faster CPU performance
  GPU support (optional)

Audio Processing
 SoundFile
 Librosa
 NumPy

Natural Language Processing
 NLTK – Sentence tokenization
 Scikit-learn
  TF-IDF vectorization
  Cosine similarity
 MMR (Maximal Marginal Relevance) – Diversity-aware keyword selection

Data Handling
 JSON
 OS / Glob utilities

 
 🔄 Workflow

1) Audio Ingestion
  Place raw podcast audio files into audio_raw/

2) Audio Preprocessing
   Noise handling
  Normalization
  Conversion to WAV format
Output → audio_preprocessed/

3) Transcription
  Fast speech-to-text using Faster-Whisper
  One transcript per audio file
Output → transcripts/

4) Segmentation
  Sentence-based segmentation
  Fixed-size semantic chunks
Output → segmented_transcripts/

5) Keyword Extraction
  TF-IDF + diversity-aware selection (MMR)
  Prevents repeated keywords across segments
Output → keywords/

6) Initial Summarization
  Extractive summarization using TF-IDF
  Produces a high-level overview of each transcript
Output → summaries/
