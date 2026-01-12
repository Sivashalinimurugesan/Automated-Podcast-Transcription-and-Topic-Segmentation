
 
# Title
Automated Medical Podcast Transcription and Topic Segmentation

## Overview

Medical podcasts have become an essential resource for healthcare professionals, students, and researchers. They provide real-world insights into diseases, treatment strategies, patient care, public health initiatives, and clinical experiences. However, these podcasts are often long, unstructured, and difficult to navigate, making it challenging to quickly extract specific information.

This project addresses these challenges by developing an AI-powered system that:

- Automatically transcribes podcast audio into text

Segments the transcript into meaningful topics

Generates concise summaries for quick understanding

Extracts important keywords and visualizes them

Performs sentiment analysis to highlight emotional tone

Provides a user-friendly interface for easy exploration

The system enables efficient navigation and comprehension of medical podcasts, saving time and improving accessibility of information.

## Approach

The system follows a pipeline-based architecture, combining speech processing and natural language processing (**NLP**) techniques. The key steps are:

3.1 Audio Input

Users can upload podcast audio in **WAV** or **MP3** format.

Supports long-duration real-world medical podcast recordings.

3.2 Speech-to-Text Transcription

Utilizes OpenAI Whisper to transcribe audio into text.

Handles noisy audio and complex medical terminology.

Ensures accurate, high-quality transcripts for further processing.

3.3 Transcript Processing & Topic Segmentation

Transcripts are split into sentences.

Sentences are grouped into logical segments representing topic changes.

Each segment corresponds to a specific discussion topic, making navigation easier.

3.4 Summarization

Summarizes each podcast into a concise 5–6 sentence paragraph.

Highlights key points, discussions, and insights from each segment.

3.5 Keyword Extraction

Extracts important medical terms, treatments, and concepts using KeyBERT.

Visualizes keywords via bar charts and word clouds.

Helps users quickly locate the most relevant concepts in the podcast.

3.6 Sentiment Analysis

Uses TextBlob to determine the sentiment of each segment.

Visualizes sentiment over time via a sentiment timeline.

Supports detection of positive, negative, or neutral discussions.

3.7 Interactive User Interface

Built with Gradio for easy use.

Features include:

Segment-wise transcript view

Keyword explorer

Summary and sentiment timeline

Search and filter functionality

## Tech Stack

Backend

Python 3.9+ – Core programming language

OpenAI Whisper – Speech-to-text transcription

**NLTK** – Sentence tokenization and text preprocessing

KeyBERT – Keyword extraction

TextBlob – Sentiment analysis

Matplotlib & WordCloud – Data visualization

Gradio – Interactive web-based UI

Frontend / UI

Gradio Blocks UI for simplicity and rapid prototyping

**HTML**-rendered charts and word clouds for clear visualization

### Supporting Libraries

NumPy – Numerical computation

SoundFile – Audio file handling

Regex – Text cleaning and pattern matching

Tempfile – Temporary file storage

5. Setup
Prerequisites

Python 3.9 or above

pip package manager

FFmpeg installed (required by Whisper)

### Installation Steps

git clone [https://github.com/your-username/Automated-Medical-Podcast-Transcription.git](https://github.com/your-username/Automated-Medical-Podcast-Transcription.git) cd Automated-Medical-Podcast-Transcription pip install -r requirements.txt

### Required Python Packages

gradio, openai-whisper, keybert, sentence-transformers, nltk, textblob, matplotlib, soundfile, wordcloud

6. Usage

Run the application:

python app.py

Open the Gradio link displayed in the terminal.

Upload a medical podcast audio file.

Click Analyze Podcast.

Explore results:

Summary tab – concise podcast overview

Keyword analytics – visualized key medical terms

Sentiment timeline – segment-wise sentiment

Keyword explorer – search specific terms

Segment-wise transcript view – explore topic segments

## Troubleshooting

When using the system, you may encounter some common issues:

Audio processing failed: Ensure the uploaded audio is clear and in **WAV** or **MP3** format. Re-exporting the audio may help.

Whisper model error: Install FFmpeg and make sure it is added to your system **PATH**. Verify with ffmpeg -version.

**NLTK** tokenizer error: Download required **NLTK** data by running:

import nltk nltk.download('punkt')

UI not loading / Gradio errors: Ensure you are using Python 3.9+ and all required packages are installed. Restart your terminal if needed.

Memory issues / Long audio processing: Use shorter audio or the Whisper small model. Close other applications to free memory.

Keywords not extracted properly: Ensure transcripts are clean and free of filler words before running keyword extraction.

Sentiment analysis seems inaccurate: TextBlob is generic and may not fully reflect medical context.

Charts or WordCloud not displayed: Ensure Matplotlib and WordCloud are installed and system backend supports rendering.

File upload fails in Gradio: Check file format, browser stability, and network connection.

## Limitations and Challenges

Sentiment analysis is generic, not fully medical-domain specific

Topic segmentation is sentence-length based, not semantic

No speaker diarization (assumes single-speaker)

Processing long podcasts may be slow on low-end systems

Frontend is Gradio prototype, not full production-ready React

## Future Scope

Medical Named Entity Recognition (**NER**) for diseases, treatments, and drugs

Speaker diarization and role detection (doctor, patient, narrator)

Semantic topic segmentation using transformer embeddings

Support for multi-language podcasts

Semantic search across multiple podcast episodes

Full React + Flask **API** production deployment

Podcast quality evaluation using **WER**, **CER**, and semantic similarity

## References

OpenAI Whisper – [https://github.com/openai/whisper](https://github.com/openai/whisper)

KeyBERT – [https://github.com/MaartenGr/KeyBERT](https://github.com/MaartenGr/KeyBERT)

**NLTK** Documentation – [https://[www.nltk.org](https://www.nltk.org](https://www.nltk.org](https://www.nltk.org))

TextBlob – [https://textblob.readthedocs.io](https://textblob.readthedocs.io)

Spotify Podcast Dataset (Kaggle)

HuggingFace Transformers – [https://huggingface.co](https://huggingface.co)

## License

This project is licensed under the **MIT** License.