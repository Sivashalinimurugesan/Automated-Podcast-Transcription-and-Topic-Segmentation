# Automated Medical Podcast Transcription and Topic Segmentation

## Project Overview

Medical podcasts contain valuable discussions on diseases, treatments, research findings, and clinical experiences. However, these podcasts are often long and difficult to navigate.

This project builds an AI-powered system that automatically transcribes medical podcast audio, detects topic boundaries, and segments the content into meaningful medical topics with summaries, keywords, sentiment analysis, and quality evaluation.

The system enables students, researchers, and healthcare professionals to quickly access relevant medical information without listening to the entire podcast episode.

---

## Use Case (Medical Domain)

This system is designed specifically for medical podcasts, including:

- Clinical discussions  
- Disease awareness talks  
- Medical education podcasts  
- Expert interviews and panel discussions  
- Public health awareness programs  

### Benefits

- Quickly locate discussions about specific diseases or symptoms  
- Navigate podcasts using topic-wise segmentation  
- Understand content through summaries, keywords, and sentiment  
- Save time for medical students and professionals  

---

## Project Objectives

### 1. Transcription (Speech-to-Text)
- Convert long medical podcast audio into text using ASR models  
- Handle noisy, real-world medical audio  
- Generate timestamps for each transcribed segment  

### 2. Topic Segmentation
- Detect topic shifts in medical discussions  
- Segment transcripts into meaningful medical chapters  
- Apply NLP techniques such as:
  - TextTiling  
  - Embedding similarity (Sentence Transformers / BERT)  
  - Change-point detection  

### 3. Summarization and Keyword Extraction
- Generate concise summaries for each segment  
- Extract domain-relevant medical keywords  

### 4. Sentiment and Quality Analysis
- Perform sentiment analysis on segmented topics  
- Normalize sentiment for medical-domain context  
- Compute quality metrics such as WER, CER, and semantic similarity  

### 5. Frontend UI for Navigation
- Topic-wise transcript visualization  
- Timestamp-based audio playback  
- Keyword, sentiment, and quality dashboards  
- Interactive UI integrated with backend APIs  

---

## System Architecture

Audio Input  
↓  
Audio Preprocessing  
↓  
Medical Speech-to-Text (ASR)  
↓  
Transcript Cleaning  
↓  
Embedding Model  
↓  
Topic Segmentation  
↓  
Medical Summaries, Keywords & Sentiment  
↓  
Quality Evaluation  
↓  
Indexing  
↓  
Frontend UI (Search, Playback, Visualization)

---

## Tech Stack

### Backend
- Python 3.9+  
- Flask  
- Whisper (OpenAI) / Faster-Whisper  
- Librosa, PyDub, FFmpeg  

### NLP and Machine Learning
- NLTK  
- SpaCy  
- HuggingFace Transformers  
- Sentence Transformers  
- KeyBERT / YAKE / RAKE  

### Frontend
- React.js  
- HTML, CSS, JavaScript  
- REST API integration  

### Visualization
- Chart.js  
- Plotly  
- Matplotlib  

### Storage
- JSON / CSV  
- SQLite (optional)  
- FAISS / Vector Database (optional)  

---

## Project Structure

```text
Automated-Podcast-Transcription-and-Topic-Segmentation/
│
├── src/
│   ├── preprocessing.py
│   ├── transcription.py
│   ├── segmentation.py
│   ├── evaluation_summary.py
│   ├── evaluation.py
│   ├── keyword_cloud.py
│   ├── keywords.py
│   ├── sentiment.py
│   ├── pipeline_controller.py
│   └── user_state_manager.py
│
├── ui_app/
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── KeywordCloudView.jsx
│       │   ├── QualityDashboard.jsx
│       │   └── SegmentSentiment.jsx
│       ├── App.js
│       └── index.js
│
├── Inference/
│   ├── transcripts/
│   ├── segments/
│   └── keywords/
│
├── notebooks/
├── docs/
├── tests/
├── README.md
├── requirements.txt
└── .env.example
## Milestone-wise Implementation

### Milestone 1: Audio Preprocessing & Transcription
- Audio normalization  
- ASR-based transcription  

### Milestone 2: Topic Segmentation & Keyword Extraction
- Topic boundary detection  
- Medical keyword extraction  

### Milestone 3: Sentiment & Quality Evaluation
- Segment-level sentiment analysis  
- WER, CER, and semantic similarity computation  

### Milestone 4: Frontend Integration & Visualization
- React-based UI  
- Topic navigation and playback  
- Keyword, sentiment, and quality dashboards  

### Milestone 5: Documentation & Final Delivery
- Technical documentation  
- Final demo and evaluation  

---

## Data and Privacy Considerations
- Raw audio and large files are not committed to the repository  
- API keys are managed using environment variables  
- Only source code and configuration files are version-controlled  

---

## Future Enhancements
- Medical entity recognition (NER)  
- Speaker diarization  
- Semantic search across episodes  
- Multi-language support  

---

## Intended Users
- Medical students  
- Healthcare professionals  
- Researchers  
- Medical educators  

---

## License
This project is licensed under the **MIT License**.
