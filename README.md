 Project Title
 --------------
 
Automated Podcast Transcription & Topic Segmentation Dashboard
--------------------------------------------------------------------------

 Overview
 ------------
 
This project provides an end-to-end pipeline to automatically process podcast audio files into meaningful textual insights. It converts audio recordings into clean transcripts, segments the content into logical topics, extracts important keywords, and visualizes insights using an interactive dashboard.
The system helps users analyze large audio datasets efficiently without manual transcription or review. The web-based UI allows easy browsing of transcripts, segmented text, keyword extraction, audio playback, and visual analytics.
This project is built using Python, Natural Language Processing (NLP), and Streamlit.

-------------------------------------------------------------------------------

Objectives
----------------

Automatically clean and preprocess raw podcast audio.
Generate text transcripts from audio recordings.
Segment long transcripts into meaningful topic sections.
Extract keywords for quick content understanding.
Provide interactive visualization of word frequencies and word clouds.
Enable playback of cleaned audio files.
Build a simple and user-friendly dashboard for analysis.

------------------------------------------------------------------
 Use Cases
 ---------
 
Podcast creators analyzing episode content.
Researchers performing speech-to-text analysis.
Students learning NLP pipelines.
Content analysts extracting important topics.
Audio archive management.
Text analytics demonstrations and academic projects.

 Approach
 -----------
 
Audio Processing
Raw audio files are stored in audio_raw.
Noise reduction and cleaning scripts generate cleaned audio in audio_processed.
Transcription
Audio files are converted into text transcripts.
Transcripts are saved in the transcripts folder.
Preprocessing
Text cleaning removes unwanted headers, footers, symbols, and noise.
Segmentation
Cleaned text is divided into meaningful segments.
Output stored in segmented folder.
Keyword Extraction
Important keywords are extracted using frequency analysis.
Results saved in keywords folder.
Visualization
Word frequency bar chart.
Word cloud visualization.
Dashboard UI
Built using Streamlit.
Users can upload files, view transcripts, segments, keywords, visualizations, and play cleaned audio.

-----------------------------------------------------------------------------------------------
project folder
-------------


project/
│
├── audio_raw/           → Raw audio input files
├── audio_processed/     → Cleaned audio output
├── transcripts/         → Generated transcripts (.txt)
├── segmented/           → Topic segmented text files
├── keywords/            → Extracted keywords files
├── script/              → Processing scripts
│     ├── audio_clean.py
│     ├── preprocess.py
│     ├── transcript.py
│     ├── segment_text.py
│     ├── extract_keywords.py
│     └── evaluate_all.py
│
├── ui/
│     └── app.py          → Streamlit dashboard
│
└── evaluation_report.xlsx

 


Usage
-------

Upload transcript file using Upload tab.
View full transcript in Transcript tab.
View segmented text in Topic Segments tab.
View extracted keywords in Keywords tab.
Explore charts and word cloud in Visualizations tab.
Listen to cleaned audio in Cleaned Audio tab.


Troubleshooting
----------------

Issue
Solution
Streamlit not found
Run pip install streamlit
No files visible
Check folder paths
Audio not playing
Ensure audio files exist in audio_processed
Charts not loading
Install matplotlib and wordcloud
Port already in use
Restart system or change port


 Limitations
 ---------------
 
Large audio files may take longer processing time.
Accuracy depends on transcription quality.
Keyword extraction is frequency-based (basic NLP).
No cloud deployment included.
Works on local machine only.


 Future Enhancements
 ----------------------
 
Real-time audio transcription.
Speaker identification.
Sentiment analysis.
Topic modeling with ML models.
Cloud deployment.
Multi-language support.
Export reports to PDF/Excel.


References
------------

Streamlit Documentation
Python NLP Tutorials
WordCloud Library
Matplotlib Documentation
GitHub Guides
