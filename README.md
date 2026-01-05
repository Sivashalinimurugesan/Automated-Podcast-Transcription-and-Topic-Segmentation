# Automated Podcast Transcription and Topic Segmentation

[cite_start]An AI-powered system designed to convert unstructured podcast audio into structured, searchable, and summarized text segments using state-of-the-art Speech-to-Text and NLP techniques[cite: 54, 68].

##  Project Overview
[cite_start]With the rapid growth of digital media, analyzing long podcast episodes manually is inefficient[cite: 53, 66]. [cite_start]This project automates transcription, segments content into topics, extracts key terms, and generates concise summaries to enhance accessibility and navigation[cite: 54, 56, 69].

---

##  Key Features
* [cite_start]**Automated Transcription**: High-accuracy speech-to-text conversion using the OpenAI Whisper model[cite: 84, 112].
* [cite_start]**Topic Segmentation**: Automatically divides transcripts into coherent sections based on semantic changes[cite: 86, 126].
* [cite_start]**Keyword Extraction**: Identifies critical terms for each segment for quick scanning[cite: 132, 134].
* [cite_start]**Summarization**: Provides brief summaries for each segment using the BART model[cite: 87, 135].
* [cite_start]**Interactive UI**: A React-based interface with an audio player synced to time-stamped segments[cite: 88, 144].

---

##  Technology Stack
| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React, Tailwind CSS | [cite_start]Building a responsive UI and managing real-time state[cite: 192]. |
| **Backend** | Flask | [cite_start]Orchestrating the API and handling file uploads[cite: 192]. |
| **AI Models** | Whisper, BART | [cite_start]Speech-to-Text and Abstractive Summarization[cite: 192]. |
| **NLP** | NLTK, Sentence Transformers | [cite_start]Tokenization, keywords, and clustering[cite: 192]. |
| **Audio** | FFmpeg, Librosa | [cite_start]Format conversion and noise cleaning[cite: 192]. |

---

##  Project Hierarchy
```text
AUTOMATED-PODCAST-TRANSCRIPTION/
├── backend/                        
[cite_start]│   ├── audio_preprocessing/        # preprocess.py (16kHz conversion) [cite: 215, 219]
[cite_start]│   ├── transcription/              # transcribe.py (Whisper Model) [cite: 230, 234]
[cite_start]│   ├── segmentation/               # segmentation.py (Topic splitting) [cite: 225, 229]
[cite_start]│   ├── data/                       # Storage for audio & JSON results [cite: 220, 236]
[cite_start]│   └── app.py                      # Main Flask API orchestrator [cite: 199, 235]
├── frontend/                       
│   ├── src/
[cite_start]│   │   ├── components/             # UI Components (UploadCard, Result, etc.) [cite: 260]
[cite_start]│   │   ├── api.js                  # Axios service layer [cite: 248, 274]
[cite_start]│   │   └── App.jsx                 # Main application state [cite: 247, 276]
│   └── package.json
├── docs/                           # Documentation folder
[cite_start]│   └── Automated-Podcast-Transcription-and-Topic-Segmentation.pdf [cite: 32, 33]
├── LICENSE                         # MIT License file
└── README.md

## System Work-Flow

[cite_start]The system follows a modular pipeline to ensure high-quality results[cite: 92, 94]:

* [cite_start]**User Upload**: Audio files in MP3, WAV, or M4A format are uploaded via the React Frontend[cite: 98, 152].
* [cite_start]**Preprocessing**: The Flask backend converts audio to 16kHz mono WAV and applies noise reduction to improve accuracy[cite: 104, 107, 109, 154].
* [cite_start]**Transcription**: The OpenAI Whisper model generates a complete, time-aligned transcript of the speech[cite: 111, 115, 155].
* [cite_start]**NLP Analysis**: The transcript is segmented into topics, and concise summaries and keywords are generated for each section[cite: 125, 132, 135, 156].
* [cite_start]**Output**: Results are packaged into a structured JSON response and sent to the frontend for visualization[cite: 137, 141, 160].



---

##  Project Documentation
For a detailed explanation of the project, including methodology and results, refer to the full report:
[cite_start] **[Download Project Report (PDF)](./docs/Automated-Podcast-Transcription-and-Topic-Segmentation.pdf)** [cite: 32, 58]

---

##  Use Cases

* [cite_start]**Audio Search Engine**: Users can search for phrases and instantly jump to exact timestamps within long-form audio[cite: 279, 283].
* [cite_start]**Accessibility**: Provides readable transcripts and summaries for hearing-impaired users and non-native speakers[cite: 291, 294, 300].
* [cite_start]**Information Retrieval**: Enables students and researchers to find precise data without listening to entire episodes[cite: 285, 287, 288].

---

##  License
This project is licensed under the **MIT License**.
Copyright (c) 2025 springboardmentor13579x-proj

> See the [LICENSE](./LICENSE) file for the full text.

---
[cite_start]**Intern**: Nidhi Paswan [cite: 10, 33]
[cite_start]**Mentor**: Mr. Goutham Nishkal [cite: 12, 41]
[cite_start]**Program**: Infosys Springboard Virtual Internship [cite: 6, 24]