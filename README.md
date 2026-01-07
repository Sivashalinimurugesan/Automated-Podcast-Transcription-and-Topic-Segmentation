Automated Podcast Transcription and Topic Segmentation
This project focuses on converting podcast/audio files into text, cleaning the transcripts, segmenting the text into meaningful parts, extracting keywords, and visualizing important insights using charts and word clouds.
It provides a simple UI where users can listen to cleaned audio, view transcripts, segmented text, extracted keywords, search keywords, and visualize word frequencies.


----------------------------------------------------------------------
📌 Project Overview
The system takes raw audio files and performs:
Audio preprocessing and cleaning
Speech-to-text transcription
Text preprocessing
Topic segmentation
Keyword extraction
Visualization of word frequency and keyword importance
User-friendly UI for interaction


----------------------------------------------------------------------
🎯 Use Cases
Podcast transcription automation
Audio content analysis
Topic discovery in long audio files
Keyword extraction for indexing/search
Educational projects
NLP research demonstrations


------------------------------------------------------------------
🌟 Benefits
Saves time compared to manual transcription
Automatically extracts meaningful insights
Helps in understanding large audio datasets
Easy visualization of important words
Search functionality for keywords
Modular and scalable project structure


---------------------------------------------------------------------
🚀 Project Objectives
Convert audio files into readable text
Clean and preprocess the transcripts
Segment text into logical parts
Extract keywords automatically
Visualize text insights using graphs and word clouds
Provide an interactive UI


-----------------------------------------------------------------
🏗️ System Architecture
Audio Input
Raw audio files stored in audio_raw/
Audio Cleaning
Noise reduction and preprocessing
Cleaned audio saved in audio_processed/
Transcription
Converts audio to text
Output stored in transcripts/
Text Preprocessing
Removes headers, footers, noise text
Segmentation
Splits text into logical segments
Output stored in segmented/
Keyword Extraction
Extracts important keywords
Output stored in keywords/
Visualization
Bar chart of word frequency
Word cloud visualization
UI
Displays audio, transcript, segments, keywords, search and visualization


---------------------------------------------------------------------------------
🛠️ Tech Stack
Programming Language: Python
Libraries:
SpeechRecognition
NLTK / spaCy
pandas
matplotlib
wordcloud
streamlit
IDE: VS Code
Version Control: GitHub


--------------------------------------------------------------------------------------
📁 Project Folder Structure
Copy code

project/
│
├── audio_raw/            → Original audio files
├── audio_processed/      → Cleaned audio files
├── transcripts/          → Generated transcripts
├── segmented/            → Segmented text files
├── keywords/             → Extracted keywords
├── ground_truth/         → Reference data
├── script/               → Python processing scripts
│   ├── transcript.py
│   ├── preprocess.py
│   ├── segment_text.py
│   ├── extract_keywords.py
│   └── audio_clean.py
│
├── ui/
│   └── app.py             → Streamlit UI
│
├── README.md
└── LICENSE


-------------------------------------------------------------

streamlit run ui/app.py
📊 Features
 Audio Playback
 Transcript Display
 Segmented Text View
 Keyword Extraction
 Keyword Search
Visualization (Bar chart & Word Cloud)
