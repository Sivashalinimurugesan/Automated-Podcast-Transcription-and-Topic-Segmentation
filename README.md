# Automated-Podcast-Transcription-and-Topic-Segmentation

An AI-powered system designed to convert unstructured podcast audio into structured, searchable, and summarized text segments using state-of-the-art Speech-to-Text and NLP techniques. 

## Project Overview
With the rapid growth of digital media, analyzing long podcast episodes manually is time-consuming and inefficient. This project automates the transcription process, segments content into meaningful topics, extracts key terms, and generates concise summaries to enhance content usability and accessibility.


## Key Features

**Automated Transcription**: Converts speech to text with high accuracy using the OpenAI Whisper model.

**Topic Segmentati**on: Automatically divides transcripts into coherent sections based on topic changes.

**Keyword Extraction**: Identifies critical terms for each segment to aid quick scanning.

**Summarization**: Provides brief summaries of each segment, allowing users to grasp main ideas without listening to the entire audio.

**Interactive UI**: A React-based interface featuring an audio player synced with time-stamped segments.


## System Architecture

The system follows a sequential pipeline from user upload to final visualization:
1. **User Upload:** Audio file (MP3, WAV, M4A) via React Frontend.
2. **Preprocessing:** Flask backend converts audio to 16kHz mono WAV and reduces noise.
3. **Transcription:** OpenAI Whisper model generates a time-aligned transcript.
4. **NLP Analysis:** Segmentation, keyword extraction, and summary generation.
5. **Output:** Structured JSON response visualized on a dashboard


##  Technology Stack

 **Frontend** :  React, Tailwind CSS 
 **Backend**  :  Flask 
 **AI Models**:  Whisper, BART
 **NLP**      :  NLTK, Sentence Transformers 
 **Audio**    :  FFmpeg, Librosa 


##  Project Hierarchy

AUTOMATED-PODCAST-TRANSCRIPTION/
├── backend/                        
│   ├── audio_preprocessing/        # preprocess.py (16kHz conversion)
│   ├── transcription/              # transcribe.py (Whisper Model)
│   ├── segmentation/               # segmentation.py (Topic splitting)
│   ├── data/                       # Storage for raw/clean audio & JSON segments
│   └── app.py                      # Main Flask API orchestrator
├── frontend/                       
│   ├── src/
│   │   ├── components/             # UploadCard, PodcastResult, Navbar
│   │   ├── api.js                  # Axios service layer
│   │   └── App.jsx                 # Main application state
│   └── package.json
└── README.md


## System Work-Flow
1. The system follows a sequential pipeline from user upload to final visualization:

2. User Upload: Audio file (MP3, WAV, M4A) via React Frontend.

3. Preprocessing: Flask backend converts audio to 16kHz mono WAV and reduces noise.

4. Transcription: Whisper model generates a time-aligned transcript.

5. NLP Analysis: Segmentation, keyword extraction, and summary generation.

6. Output: Structured JSON response sent to the frontend for display.


## Use Cases

**Audio Search Engine**: Locate specific words or phrases within long audio files instantly.

**Accessibility**: Providing text versions and summaries for hearing-impaired users.

**Information Retrieval**: Helping students and researchers find precise information in lengthy discussions quickly.