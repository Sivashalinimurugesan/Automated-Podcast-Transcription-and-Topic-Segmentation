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

```text
AUTOMATED-PODCAST-TRANSCRIPTION/
├── backend/                        
[cite_start]│   ├── audio_preprocessing/        # preprocess.py (16kHz conversion) [cite: 154, 215, 219]
[cite_start]│   ├── transcription/              # transcribe.py (Whisper Model) [cite: 155, 230, 234]
[cite_start]│   ├── segmentation/               # segmentation.py (Topic splitting) [cite: 156, 225, 229]
[cite_start]│   ├── data/                       # Storage for raw/clean audio & JSON segments [cite: 138, 220, 236]
[cite_start]│   └── app.py                      # Main Flask API orchestrator [cite: 153, 199, 235]
├── frontend/                       
│   ├── src/
[cite_start]│   │   ├── components/             # UploadCard, PodcastResult, Navbar, Hero [cite: 152, 251, 260]
[cite_start]│   │   ├── api.js                  # Axios service layer [cite: 248, 274]
[cite_start]│   │   └── App.jsx                 # Main application state [cite: 247, 276]
│   └── package.json
└── README.md

```
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

---

##  License

This project is licensed under the **MIT License**.

Copyright (c) 2025 springboardmentor13579x-proj

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files... (and so on)

> See the [LICENSE](./LICENSE) file for the full text.

**Information Retrieval**: Helping students and researchers find precise information in lengthy discussions quickly.
