
# Automated-Podcast-Transcription-and-Topic-Segmentation

*A Springboard Internship Program Project*

---

## 📌 Project Overview

The **Automated Podcast Transcription & Topic Segmentation** project aims to build an end-to-end AI system that can:

- Convert podcast audio into accurate transcripts  
- Detect topic boundaries automatically  
- Segment the transcript into meaningful chapters  
- Extract keywords and summaries for each topic  
- Provide a UI to navigate the podcast episode by topics & timestamps  
- Display segment-level visual analytics  

This project focuses on applying **AI, Speech Processing, NLP, and Machine Learning** engineering to create a practical real-world audio intelligence system.

---

## 🎯 Project Objectives

- Build a reliable audio preprocessing and transcription pipeline  
- Implement topic segmentation using NLP techniques  
- Generate summaries and keywords for each detected topic  
- Design a backend pipeline to integrate all components  
- Create a user-friendly interface for podcast exploration  

---

## 🧠 System Architecture

1. **Audio Cleaning**  
   - Noise reduction  
   - Silence trimming  
   - Audio normalization  

2. **Speech-to-Text Transcription**  
   - Convert cleaned audio into text transcripts  

3. **Text Segmentation**  
   - Detect topic boundaries  
   - Segment transcripts into chapters  

4. **Keyword Extraction & Summarization**  
   - Extract important keywords  
   - Generate concise summaries  

5. **Visualization & UI**  
   - Topic-wise navigation  
   - Timestamp-based exploration  

---

## 📂 Project Structure

```text
├── client/
├── audio_cleaner.py
├── audio_transcriber.py
├── text_segmenter.py
├── summarizer.py
├── run_pipeline.py
├── server.py
├── config.py
├── fix_config.py
├── package.json
├── package-lock.json
├── LICENSE
├── README.md
