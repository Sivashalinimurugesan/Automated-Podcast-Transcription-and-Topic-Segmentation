

\# Automated Podcast Transcription and Topic Segmentation

\## Documentation Report



---



\## 1. Introduction



This project presents an end-to-end Artificial Intelligence system for \*\*automatic transcription, topic segmentation, keyword extraction, sentiment analysis, and visualization\*\* of long-form spoken content. The system is designed primarily for \*\*HR interviews\*\*, and can also be applied to \*\*corporate meetings, podcasts, webinars, and academic lectures\*\*.



The objective is to transform unstructured audio into structured, searchable, and analyzable text using a modular processing pipeline and an interactive Streamlit-based user interface.



---



\## 2. System Architecture



The system follows a modular pipeline where each component performs a dedicated task:



```

Audio Input

&nbsp;  |

&nbsp;  v

Audio Preprocessing

&nbsp;  |

&nbsp;  v

Automatic Speech Recognition (Whisper)

&nbsp;  |

&nbsp;  v

Topic Segmentation

&nbsp;  |

&nbsp;  v

Summarization \& Keyword Extraction

&nbsp;  |

&nbsp;  v

Sentiment \& Evaluation

&nbsp;  |

&nbsp;  v

Visualization \& Streamlit UI

```



Each module is independently testable and extensible.



---



\## 3. Methodology



\### 3.1 Audio Preprocessing

\- Input audio is converted into a standard format and sampling rate.

\- Noise reduction and normalization improve ASR accuracy.

\- Output is stored in `audio\_processed/`.



\### 3.2 Automatic Speech Recognition (ASR)

\- Implemented using \*\*OpenAI Whisper\*\*.

\- Converts audio to text while handling conversational speech.

\- Output transcripts are saved in `transcripts/asr/`.



\### 3.3 Topic Segmentation

\- The transcript is divided into meaningful discussion segments.

\- Segments represent coherent conversational units.

\- Stored in the `segments/` directory.



\### 3.4 Summarization

\- Extractive summarization identifies the most relevant sentences.

\- Produces concise overviews of each audio file.

\- Saved in `transcripts/final/`.



\### 3.5 Keyword Extraction

\- Uses TF-IDF with n-grams (1–2).

\- Filters noise and duplicates.

\- Focuses on HR-related and professional keywords.

\- Results saved in `docs/keywords.txt`.



\### 3.6 Sentiment and Emotion Analysis

\- Each segment is analyzed using \*\*VADER sentiment scoring\*\*.

\- Produces polarity scores and overall emotional tone.



\### 3.7 ASR Evaluation

\- Word Error Rate (WER) and accuracy are computed.

\- Metrics saved in:

&nbsp; - `docs/asr\_evaluation.csv`

&nbsp; - `docs/asr\_evaluation\_table.txt`



---



\## 4. Implementation Details



\### Technology Stack



| Component              | Tools / Libraries                     |

|-----------------------|---------------------------------------|

| Programming Language | Python 3.12                           |

| ASR                  | OpenAI Whisper                        |

| Audio Processing     | Librosa, PyDub, FFmpeg                |

| NLP                  | NLTK, Scikit-learn                    |

| Visualization        | Streamlit, Plotly, Matplotlib         |

| Keyword Cloud        | WordCloud                             |

| Evaluation           | jiwer                                 |

| Testing              | PyTest                                |



---



\## 5. Directory Structure



```

Automated-Podcast-Transcription-and-Topic-Segmentation/

│

├── audio\_raw/

├── audio\_processed/

├── transcripts/

│   ├── asr/

│   └── final/

├── segments/

├── docs/

│   ├── keywords.txt

│   ├── asr\_evaluation.csv

│   └── asr\_evaluation\_table.txt

├── src/

│   ├── preprocessing.py

│   ├── transcription.py

│   ├── segmentation.py

│   ├── summarization.py

│   ├── keyword\_extraction.py

│   ├── evaluate\_asr.py

│   ├── core.py

│   ├── ui\_app.py

│   └── main.py

├── tests/

│   └── test\_core\_functions.py

└── README.md

```



---



\## 6. Backend Execution Results



The pipeline was executed on the audio file:



```

BoZpcibb-JI.wav

```



\### Generated Outputs



| Output Type        | Directory / File Path                    |

|-------------------|------------------------------------------|

| ASR Transcript    | `transcripts/asr/BoZpcibb-JI.txt`         |

| Segments          | `segments/BoZpcibb-JI.txt`                |

| Summary           | `transcripts/final/BoZpcibb-JI.txt`       |

| Keywords          | `docs/keywords.txt`                      |

| Evaluation (CSV)  | `docs/asr\_evaluation.csv`                |

| Evaluation (TXT)  | `docs/asr\_evaluation\_table.txt`          |



\### ASR Performance



| Metric  | Value  |

|---------|--------|

| WER     | 0.2099 |

| Accuracy| 79.01% |



---



\## 7. Streamlit User Interface



The project includes a professional, interactive dashboard built with \*\*Streamlit\*\*.



\### UI Features



\- \*\*Audio Upload \& Playback\*\*

\- \*\*Full Transcript Viewer\*\*

\- \*\*Segmented Conversation with Audio Clips\*\*

\- \*\*Keyword-Based Search\*\*

\- \*\*Keyword Word Cloud\*\*

\- \*\*Sentiment Trend Plot\*\*

\- \*\*Speaker-wise Sentiment Comparison\*\*

\- \*\*Automated AI Summary\*\*



\### Visualization Components



1\. \*\*Sentiment Trend Line Chart\*\*

&nbsp;  - Shows sentiment score across segments.

2\. \*\*Speaker Distribution Histogram\*\*

&nbsp;  - Displays conversation contribution.

3\. \*\*Speaker-wise Sentiment Bar Chart\*\*

&nbsp;  - Compares interviewer, candidate, and narrator tones.

4\. \*\*Keyword Cloud\*\*

&nbsp;  - Visual representation of extracted keywords.



---



\## 8. Use Cases



\### 8.1 HR Interviews

\- Automated transcription

\- Topic-based navigation

\- Keyword extraction for skills and experience

\- Sentiment-based candidate evaluation

\- Structured interview reports



\### 8.2 Corporate Meetings

\- Decision and agenda tracking

\- Speaker participation analysis

\- Sentiment trends across discussions



\### 8.3 Podcasts and Webinars

\- Topic chaptering

\- Content indexing

\- Listener-friendly summaries



\### 8.4 Academic Lectures

\- Segment-wise concept extraction

\- Searchable learning material

\- Accessibility support



---



\## 9. Testing and Validation



\- Unit tests implemented using \*\*PyTest\*\*.

\- Continuous Integration using \*\*GitHub Actions\*\*.

\- Validates:

&nbsp; - Segmentation

&nbsp; - Summarization

&nbsp; - Keyword extraction

&nbsp; - Sentiment analysis



---



\## 10. Limitations



\- ASR accuracy decreases in noisy environments.

\- Topic boundaries may miss subtle transitions.

\- Summarization is extractive, not abstractive.

\- Large audio files cannot be stored directly on GitHub.

\- Real-time processing is not supported.



---



\## 11. Future Enhancements



\- Multi-speaker diarization

\- Semantic search using embeddings

\- Emotion and confidence detection

\- Abstractive summarization

\- Cloud deployment (Streamlit Cloud)

\- YouTube audio ingestion



---



\## 12. Conclusion



This project demonstrates a complete pipeline for converting spoken content into structured, analyzable information. By integrating \*\*speech recognition, NLP, sentiment analysis, and interactive visualization\*\*, the system provides a scalable solution for HR interview analysis and other professional audio use cases. The Streamlit dashboard further enhances usability by enabling keyword-driven exploration, sentiment interpretation, and audio playback at the segment level.



---



\## 13. References



1\. Radford, A., et al. (2022). \*Whisper: Robust Speech Recognition via Large-Scale Weak Supervision\*. OpenAI.

2\. JiWER: https://github.com/jitsi/jiwer

3\. Hearst, M. (1997). \*TextTiling: Segmenting Text into Multi-Paragraph Subtopic Passages\*. Computational Linguistics.

4\. NLTK: https://www.nltk.org/

5\. Streamlit: https://streamlit.io/



