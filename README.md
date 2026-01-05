# Automated Podcast Transcription and Topic Segmentation

An AI-powered system designed to convert unstructured podcast audio into structured, searchable, and summarized text segments using state-of-the-art Speech-to-Text and NLP techniques.

## Project Overview
With the rapid growth of digital media, analyzing long podcast episodes manually is inefficient. This project automates transcription, segments content into topics, extracts key terms, and generates concise summaries to enhance accessibility and navigation.

## Key Features
* **Automated Transcription**: High-accuracy speech-to-text conversion using the OpenAI Whisper model.
* **Topic Segmentation**: Automatically divides transcripts into coherent sections based on semantic changes.
* **Keyword Extraction**: Identifies critical terms for each segment for quick scanning.
* **Summarization**: Provides brief summaries for each segment using the BART model.
* **Interactive UI**: A React-based interface with an audio player synced to time-stamped segments.

## Technology Stack
| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React, Tailwind CSS | Building a responsive UI and managing real-time state. |
| **Backend** | Flask | Orchestrating the API and handling file uploads. |
| **AI Models** | Whisper, BART | Speech-to-Text and Abstractive Summarization. |
| **NLP** | NLTK, Sentence Transformers | Tokenization, keywords, and clustering. |
| **Audio** | FFmpeg, Librosa | Format conversion and noise cleaning. |

## Project Hierarchy
```text
AUTOMATED-PODCAST-TRANSCRIPTION/
├── backend/                        
│   ├── audio_preprocessing/        # preprocess.py (16kHz conversion)
│   ├── transcription/              # transcribe.py (Whisper Model)
│   ├── segmentation/               # segmentation.py (Topic splitting)
│   ├── data/                       # Storage for audio & JSON results
│   └── app.py                      # Main Flask API orchestrator
├── frontend/                       
│   ├── src/
│   │   ├── components/             # UI Components (UploadCard, Result, etc.)
│   │   ├── api.js                  # Axios service layer
│   │   └── App.jsx                 # Main application state
│   └── package.json
├── docs/                           # Documentation folder
│   └── Automated-Podcast-Transcription-and-Topic-Segmentation.pdf
├── LICENSE                         # MIT License file
└── README.md
```
## System Work-Flow

The system follows a modular pipeline to ensure high-quality results:

**User Upload**: Audio files in MP3, WAV, or M4A format are uploaded via the React Frontend.
**Preprocessing**: The Flask backend converts audio to 16kHz mono WAV and applies noise reduction to improve accuracy.
**Transcription**: The OpenAI Whisper model generates a complete, time-aligned transcript of the speech.
**NLP Analysis**: The transcript is segmented into topics, and concise summaries and keywords are generated for each section.
**Output**: Results are packaged into a structured JSON response and sent to the frontend for visualization.



---

##  Project Documentation
For a detailed explanation of the project, including methodology and results, refer to the full report:
**[Download Project Report (PDF)](./docs/Automated-Podcast-Transcription-and-Topic-Segmentation.pdf)** 

---

##  Use Cases

**Audio Search Engine**: Users can search for phrases and instantly jump to exact timestamps within long-form audio.
**Accessibility**: Provides readable transcripts and summaries for hearing-impaired users and non-native speakers.
**Information Retrieval**: Enables students and researchers to find precise data without listening to entire episodes.

---

##  License
This project is licensed under the **MIT License**.
Copyright (c) 2025 springboardmentor13579x-proj

> See the [LICENSE](./LICENSE) file for the full text.

---
