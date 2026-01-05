# Automated Podcast Transcription and Topic Segmentation

## I. Overview

This project provides an **end-to-end AI-powered pipeline** to automatically convert **meeting or podcast audio** into accurate text transcripts, followed by **topic-based segmentation, summarization, keyword extraction, and sentiment analysis** using modern Natural Language Processing (NLP) techniques.

It is designed to efficiently process **long-form audio content** and is suitable for real-world applications such as:

- Automated meeting minutes
- Podcast summarization
- Interview analysis
- Research documentation

---

## Objectives

-  Convert audio recordings into accurate text transcripts using **OpenAI Whisper**
-  Segment long conversations into meaningful topics using **semantic analysis**
-  Generate concise summaries for each identified topic segment
-  Extract important keywords for quick content understanding
-  Visualize sentiment trends and timelines through an interactive dashboard

---

## Key Features

- **Automatic Speech Recognition (ASR)**  
  High-accuracy transcription using **OpenAI Whisper**

- **Topic Segmentation**  
  Semantic topic detection using **TF-IDF** and **Cosine Similarity**

- **Summary Generation**  
  AI-based summarization using **HuggingFace Transformers (DistilBART)**

- **Keyword Extraction**  
  Important keyword identification using **TF-IDF ranking**

- **Sentiment Analysis**  
  Emotional tone analysis using **NLTK VADER**

- **Optimized for Long Audio**  
  Designed to handle long meeting and podcast recordings efficiently

---

## Dataset

This project was developed and tested using a subset of the **TED Talks Audio Dataset**.

- **Source:** Kaggle – TED Talks Audio Dataset  
- **Nature:** Real-world educational and conversational audio recordings  
- **Use Case:** Suitable for long-form transcription and topic segmentation tasks



## Tech Stack

- **Python 3.9+**
- **OpenAI Whisper** – Speech-to-text transcription
- **NLTK** – Sentence tokenization & sentiment analysis
- **Scikit-learn** – TF-IDF vectorization & cosine similarity
- **HuggingFace Transformers** – Text summarization (DistilBART)
- **Streamlit** – Interactive dashboard UI
- **Plotly** – Data visualization

---

## Use Cases

### Automated Meeting Minutes
Converts recorded meetings into structured transcripts with topic-wise summaries, enabling faster review and better documentation.

### Podcast and Media Analysis
Helps podcasters and content creators analyze long episodes using AI-generated summaries, extracted keywords, and sentiment trends.

### Interview and Research Analysis
Useful for journalists, researchers, and HR teams to efficiently analyze interviews and qualitative research recordings.

### Educational Content Indexing
Enables semantic indexing of lectures, talks, and seminars, allowing quick content search and improved knowledge accessibility.

### Enterprise Knowledge Management
Supports organizations in organizing, analyzing, and retrieving insights from large volumes of internal audio data.

---


## Project Structure

```text
AUTOMATED-PODCAST-TRANSCRIPTION/
│
├── data/                         # Auto-generated Data Storage
│   ├── audio/                    # Raw Input Audio
│   ├── processed_audio/          # 16kHz Mono WAV Files
│   ├── transcripts/              # JSON Transcripts with timestamps
│   ├── semantic_segments/        # Topic Segmentation Reports
│   ├── sentiment_data/           # Sentiment scores for visualization
│   ├── short_summary/            # AI-generated summaries
│   └── keywords/                 # Extracted keywords
│
├── src/                          # Source Code
│   ├── dashboard.py              # Streamlit Dashboard (Frontend)
│   ├── podcast_backend.py        # Master AI Processing Pipeline
│   └── __init__.py
│
├── docs/                         # Documentation
├── images/                       # Screenshots for README
├── tests/                        # Unit Tests
│
├── .env                          # Environment Variables
├── requirements.txt              # Dependency Management
├── README.md                     # Project Documentation
└── LICENSE
