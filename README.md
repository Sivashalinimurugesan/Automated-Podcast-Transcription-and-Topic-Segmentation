🎙️ Automated Podcast Transcription & Topic Segmentation

I. Overview

This project provides an end-to-end AI system designed to unlock the value hidden in long-form audio. By applying advanced Speech Processing and NLP techniques, this tool automatically transcribes podcasts, segments them into coherent chapters, analyzes emotional tone, and provides a searchable, interactive dashboard for navigation. It is designed to efficiently process long-form audio suitable for real-world applications such as automated meeting minutes, podcast summarization, and interview analysis.

II. Objectives

Transcription (Speech-to-Text)

Convert long podcast audio files into accurate text using OpenAI's Whisper model.

Generate precise timestamps for each transcribed segment to enable timeline visualization.

Support noisy, multi-speaker, real-world audio.

Topic Segmentation

Detect shifts in content and break the transcript into meaningful chapters.

Use TF-IDF Vectorization and Cosine Similarity to mathematically identify topic boundaries.

Summarization & Intelligence

Generate abstractive summaries for each segment using DistilBART (Hugging Face).

Extract unique Keywords using TF-IDF ranking.

Analyze emotional tone using VADER Sentiment Analysis.

UI for Navigation & Visualization

Provide a Streamlit dashboard for uploading and processing audio.

Visualize segment-level analytics like sentiment trends over time with interactive Plotly charts.

Allow users to jump to specific topics and search transcripts instantly.

III. Key Features

Automatic Speech Recognition (ASR): High-accuracy transcription using OpenAI Whisper.

Topic Segmentation: Automatically detects natural topic boundaries in long conversations.

Smart Summarization: Generates concise abstractive summaries for every detected chapter.

Sentiment Analysis: Tracks the emotional journey (Positive/Negative/Neutral) of the speaker over time.

Keyword Extraction: Identifies key themes and tags for quick content discovery.

Interactive Dashboard: A modern UI to upload files, visualize data, and navigate transcripts.

IV. Dataset

This project was developed and tested using a subset of the TED Talks dataset sourced from Kaggle, ensuring robustness across diverse speakers and topics.

Source: TED Talks Audio (Kaggle)

Data Type: Real-world educational and conversational audio recordings.

V. Tech Stack

Core

Python 3.9+

OpenAI Whisper: State-of-the-art ASR model.

Librosa / Soundfile: Audio loading, resampling, and normalization.

FFmpeg: System-level audio processing engine.

NLP & AI

Hugging Face Transformers: sshleifer/distilbart-cnn-12-6 for summarization.

Scikit-Learn: TF-IDF Vectorizer, Cosine Similarity.

NLTK: VADER for sentiment, Punkt for sentence tokenization.

Visualization & UI

Streamlit: Interactive web application framework.

Plotly Express: Interactive charts (Sentiment Timeline, Pie Charts).

Storage

JSON: Structured storage for transcripts, segments, and analysis data.

TXT: Human-readable summaries and logs.

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
│   ├── download_kaggle_subset.py # Utility: Data acquisition script
│   └── __init__.py
│
├── docs/                      # Documentation
├── tests/                     # Unit Tests
├── .env                       # Environment Variables
├── requirements.txt           # Dependency management
├── README.md                  # Project Documentation
└── LICENSE


VII. How to Run the Project

1. Clone the Repository

git clone [https://github.com/your-username/Automated-Podcast-Transcription.git](https://github.com/your-username/Automated-Podcast-Transcription.git)
cd Automated-Podcast-Transcription


2. Create Virtual Environment (Optional but Recommended)

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


(Note: Ensure FFmpeg is installed on your system path)

4. Run the Dashboard

streamlit run src/dashboard.py


The application will open in your browser at http://localhost:8501.

VIII. System Architecture

graph TD
    A[Audio Input (File/URL)] --> B(Preprocessing: 16kHz Mono WAV);
    B --> C{AI Pipeline};
    C --> D[Transcription: OpenAI Whisper];
    C --> E[Sentiment: NLTK VADER];
    D --> F[NLP Processing];
    F --> G[Topic Segmentation: TF-IDF + Cosine Sim];
    F --> H[Summarization: DistilBART];
    F --> I[Keyword Extraction: TF-IDF];
    G --> J[Dashboard: Streamlit + Plotly];
    H --> J;
    I --> J;
    E --> J;


IX. Project Workflow & Milestones

The project implementation follows an 8-week modular roadmap:

Milestone 1

Week 1: Project Initialization and Dataset Acquisition. Defined scope and downloaded TED Talks dataset.

Week 2: Audio Preprocessing and Speech-to-Text. Implemented audio cleaning and Whisper transcription.

Milestone 2

Week 3: Topic Segmentation Implementation. Developed TF-IDF/Cosine Similarity algorithms for segmentation.

Week 4: User Interface and Indexing. Built the Streamlit app with search and navigation.

Milestone 3

Week 5: Visualization and Detail Enhancements. Added interactive Plotly timelines and sentiment analysis.

Week 6: System Testing and Feedback Collection. Refined UI based on user experience testing.

Milestone 4

Week 7: Final Documentation and Presentation Preparation. Compiled technical guides and user manuals.

Week 8: Project Wrap-up and Delivery. Final polish and submission.

X. Evaluation Criteria

The success of the project is measured against the following criteria:

Completion of Milestones: Successful implementation of audio processing, transcription, segmentation, UI, visualization, and documentation.

Transcription and Segmentation Accuracy: Quality of speech-to-text conversion and precision of topic boundaries relative to natural conversation shifts.

User Experience and Documentation Quality: Clarity and usability of the interface (Dashboard responsiveness, ease of navigation), plus well-structured, thorough project documentation.

XI. Use Cases

Podcast Analytics: Understand listener engagement and content structure.

Meeting Minutes: Automatically generate summaries and action items from meeting recordings.

Content Indexing: Make large audio archives searchable by topic and keyword.

Sentiment Tracking: Monitor the tone of conversations in interviews or customer support calls.
