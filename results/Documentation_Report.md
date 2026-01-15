\# Automated Podcast Transcription and Topic Segmentation  

\## An AI-Based System for HR Interviews, Corporate Meetings, and Spoken Content Analysis



\*\*Author:\*\* Vanshika Kumawat  

\*\*Branch:\*\* intern-vanshika  

\*\*Repository:\*\* Automated-Podcast-Transcription-and-Topic-Segmentation  

\*\*Date:\*\* January 2026  



---



\## Abstract



This project presents an end-to-end Artificial Intelligence system for the automatic transcription, topic segmentation, summarization, and analytical visualization of spoken content such as HR interviews, corporate meetings, podcasts, and academic lectures. The system integrates automatic speech recognition using OpenAI Whisper, natural language processing for segmentation and keyword extraction, sentiment analysis for emotional insights, and an interactive Streamlit-based dashboard for real-time exploration. Experimental evaluation on real interview audio demonstrates reliable transcription accuracy, effective topic discovery, and structured reporting, enabling scalable analysis of unstructured audio data in professional and organizational contexts.



---



\## 1. Introduction



Spoken content in the form of interviews, meetings, and recorded discussions is widely used in recruitment, performance evaluation, compliance, and knowledge management. However, such data is inherently unstructured and difficult to analyze at scale. Manual review is time-consuming, subjective, and inefficient for large organizations.



The objective of this project is to design and implement an automated pipeline that:



\- Converts audio into accurate textual transcripts  

\- Segments long conversations into meaningful topical units  

\- Extracts domain-relevant keywords  

\- Generates structured summaries  

\- Computes sentiment and emotional indicators  

\- Presents results through an interactive analytical dashboard  



The primary focus of this work is on \*\*HR interview analysis\*\*, where structured interpretation of candidate responses, emotional tone, and discussion flow is critical for fair and scalable evaluation.



---



\## 2. System Architecture



The system is organized as a modular processing pipeline, enabling independent development, evaluation, and future extension of each component.



```

Audio Input → Preprocessing → ASR Transcription → Topic Segmentation

&nbsp;                  ↓

&nbsp;         Summarization \& Keyword Extraction

&nbsp;                  ↓

&nbsp;     Evaluation, Visualization \& Interactive UI

```



Each stage consumes the output of the previous stage and produces structured artifacts stored in dedicated directories.



---



\## 3. Methodology



\### 3.1 Audio Preprocessing

\- Converts audio to a standardized sampling rate and format  

\- Applies noise reduction and amplitude normalization  

\- Ensures consistent input quality for automatic speech recognition  



\### 3.2 Automatic Speech Recognition (ASR)

\- Utilizes \*\*OpenAI Whisper\*\* for robust transcription of conversational speech  

\- Handles accents, varied speaking styles, and multi-speaker dialogue  

\- Produces timestamp-aligned transcripts  



\### 3.3 Topic Segmentation

\- Divides transcripts into coherent segments based on sentence structure and semantic cues  

\- Each segment represents a focused unit of discussion such as experience, skills, or project work  



\### 3.4 Summarization

\- Performs extractive summarization at both segment and document level  

\- Removes filler content and emphasizes informative statements  



\### 3.5 Keyword Extraction

\- Applies TF-IDF with domain-aware filtering  

\- Eliminates redundancy using duplicate phrase removal  

\- Prioritizes HR-relevant terms such as interview, role, experience, skills, company, communication  



\### 3.6 Sentiment and Emotion Analysis

\- Uses NLTK VADER sentiment scoring  

\- Assigns polarity scores to each segment  

\- Enables speaker-wise emotional trend comparison  



\### 3.7 Transcription Evaluation

\- Computes Word Error Rate (WER) and accuracy using the jiwer library  

\- Quantifies ASR quality against reference transcripts  



\### 3.8 Visualization and Reporting

\- Interactive dashboard implemented in Streamlit  

\- Segment-wise audio playback  

\- Keyword-based navigation  

\- Sentiment trend plots and speaker analytics  

\- Automated interview summaries  



---



\## 4. Technology Stack



\### Core Technologies

\- Python 3.12  

\- OpenAI Whisper (Automatic Speech Recognition)  

\- PyDub, Librosa, FFmpeg (Audio Processing)  



\### Natural Language Processing

\- NLTK  

\- Scikit-learn  

\- TF-IDF Vectorization  



\### Visualization and Interface

\- Streamlit  

\- Plotly  

\- Matplotlib  

\- WordCloud  



\### Evaluation and Reporting

\- jiwer (Word Error Rate)  

\- ReportLab (PDF generation support)  

\- CSV and TXT report outputs  



---



\## 5. Experimental Setup



\### 5.1 Input Audio



The system was evaluated using a real HR interview audio file:



```

audio\_raw/BoZpcibb-JI.wav

```



\### 5.2 Execution Commands



```bash

python -m src.main

streamlit run src/ui\_app.py

```



---



\## 6. Generated Outputs



After successful execution of the backend pipeline, the following structured artifacts were produced:



```

transcripts/asr/BoZpcibb-JI.txt        → Raw ASR transcript

segments/BoZpcibb-JI.txt              → Topic-segmented transcript

transcripts/final/BoZpcibb-JI.txt     → Final summarized transcript

docs/keywords.txt                     → Extracted keywords

docs/asr\_evaluation.csv               → Evaluation metrics (CSV)

docs/asr\_evaluation\_table.txt         → Evaluation report (TXT)

```



These outputs are automatically generated and can be used for further analysis, reporting, and visualization.



---



\## 7. Evaluation Results



\### 7.1 ASR Performance



Based on the evaluation file:



```

docs/asr\_evaluation\_table.txt

```



The system achieved the following performance:



| Metric | Value |

|--------|-------|

| Word Error Rate (WER) | 0.2099 |

| Accuracy | 79.01% |



This demonstrates reliable transcription performance for conversational HR interview audio.



---



\### 7.2 Keyword Extraction Results



Sample extracted keywords from the interview include:



```

interview, candidate, experience, role, company, skills, communication,

project, responsibility, career

```



These keywords accurately reflect HR-relevant discussion topics and enable targeted navigation of the transcript.



---



\### 7.3 Topic Segmentation



The interview was segmented into structured conversational units, enabling:



\- Efficient navigation across interview stages  

\- Keyword-based filtering of relevant sections  

\- Direct access to corresponding audio clips  



Each segment is associated with start and end timestamps, supporting precise playback.



---



\### 7.4 Sentiment and Emotional Analysis



The system computes sentiment polarity for each segment and aggregates speaker-wise statistics. The analysis enables:



\- Identification of emotional tone across the interview timeline  

\- Comparison between interviewer and candidate communication patterns  

\- Quantitative indicators of confidence, neutrality, or negativity  



---



\## 8. Streamlit Dashboard (User Interface)



An interactive dashboard was developed using Streamlit to visualize and explore the analytical outputs.



\### 8.1 Dashboard Features



\- Audio upload and playback  

\- One-click transcription and analysis  

\- Segmented transcript with timestamps  

\- Keyword-based search with associated audio clips  

\- Sentiment trend visualization over segments  

\- Speaker distribution plots  

\- Keyword WordCloud visualization  

\- Automated interview summary  



\### 8.2 Visualization Components



The UI includes multiple analytical plots:



\- \*\*Sentiment Trend Plot:\*\* Displays sentiment polarity across conversation segments  

\- \*\*Speaker Distribution:\*\* Shows the proportion of interviewer, candidate, and narrator segments  

\- \*\*Speaker-wise Sentiment Impact:\*\* Bar chart of average sentiment per speaker  

\- \*\*Keyword WordCloud:\*\* Visual representation of top extracted keywords  



These visualizations transform raw transcripts into interpretable analytical insights for decision-making.



---



\## 9. Use Case Validation



\### 9.1 HR Interviews

\- Automated transcription of candidate responses  

\- Structured segmentation into interview phases  

\- Keyword extraction for job-related competencies  

\- Sentiment-based behavioral analysis  

\- Objective, scalable interview evaluation  



\### 9.2 Corporate Meetings

\- Agenda-driven segmentation  

\- Decision and outcome tracking  

\- Sentiment trend monitoring  



\### 9.3 Podcasts and Webinars

\- Topic-based navigation  

\- Keyword indexing  

\- Content summarization  



\### 9.4 Academic Lectures

\- Modular segmentation  

\- Key concept extraction  

\- Learning support  



\### 9.5 Accessibility

\- Text-based access for hearing-impaired users  

\- Enhanced information retrieval from spoken content  



---



\## 10. Limitations



\- ASR accuracy may degrade in noisy environments or with strong accents  

\- Topic boundaries may miss subtle semantic transitions  

\- Summarization is extractive rather than abstractive  

\- Processing is batch-based and not real-time  

\- Large audio files are excluded from version control  



---



\## 11. Future Scope



\- Multi-speaker diarization using embeddings  

\- Transformer-based abstractive summarization  

\- Semantic search using vector databases  

\- Advanced emotion and confidence detection  

\- Cloud deployment of the dashboard  

\- Direct YouTube audio ingestion  



---



\## 12. Conclusion



This project demonstrates a complete AI-driven framework for transforming unstructured spoken content into structured, searchable, and analyzable information. By integrating Whisper-based speech recognition, NLP-based segmentation and keyword extraction, sentiment analysis, and a professional interactive dashboard, the system provides a scalable solution for HR interview analysis, organizational communication, and content intelligence.



The experimental results validate the effectiveness of the pipeline and its applicability in real-world professional environments, making it a strong foundation for further research and enterprise deployment.



---



\## 13. References



1\. Radford, A., et al. (2022). \*Whisper: Robust Speech Recognition via Large-Scale Weak Supervision\*. OpenAI.  

2\. JiWER: https://github.com/jitsi/jiwer  

3\. Hearst, M. (1997). \*TextTiling\*. Computational Linguistics.  

4\. NLTK: https://www.nltk.org/  

5\. HuggingFace: https://huggingface.co/  

6\. Streamlit: https://streamlit.io/  



