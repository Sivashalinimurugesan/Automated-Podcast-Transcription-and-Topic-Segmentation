
# Automated Podcast Transcription and Topic Segmentation

## 1. Overview
This project is an AI-powered application designed to streamline the consumption of audio content. It automates the process of transcribing podcast audio into text, segments the content based on topic shifts, and visualizes key themes. The tool allows users to upload audio files and receive a structured summary, complete with keyword insights and interactive visualizations, making it easier to navigate long-form audio content without listening to the entire file.

## 2. Approach
The application follows a linear, modular pipeline designed to convert raw unstructured audio into structured, actionable insights. The system architecture is divided into four distinct phases:

### Phase 1: Audio Ingestion & Preprocessing
Before any AI processing, the raw audio file must be normalized to ensure compatibility with the models.
* **Input:** The system accepts `.mp3` or `.wav` files via the Streamlit interface.
* **Normalization:** We use **FFmpeg** to convert all inputs to a standard format:
    * **Sample Rate:** 16,000 Hz (required by Whisper).
    * **Channels:** Mono (to reduce processing load).
    * **Bitrate:** 128 kbps.

### Phase 2: Transcription (Speech-to-Text)
We utilize OpenAI’s **Whisper** model (base/medium architecture) for the core transcription task.
* **Log-Mel Spectrogram:** The normalized audio is converted into a visual representation (spectrogram) of frequencies over time.
* **Encoder-Decoder Transformer:**
    * The **Encoder** analyzes the audio features.
    * The **Decoder** predicts the corresponding text tokens, handling language detection and punctuation automatically.
* **Result:** A highly accurate, time-stamped text transcript.

### Phase 3: Topic Segmentation & NLP Analysis
Once we have raw text, we apply Natural Language Processing (NLP) to make it navigable.
* **TextTiling Algorithm:** We use the NLTK library to analyze "lexical cohesion." The algorithm looks for shifts in vocabulary usage (e.g., stopping the use of "weather" words and starting "sports" words) to insert boundaries where the topic changes.
* **Keyword Extraction:**
    * **Stopword Removal:** Common words like "the," "is," and "and" are removed.
    * **Frequency Analysis:** We calculate the most frequent meaningful nouns and verbs to represent the core themes of the podcast.

### Phase 4: Visualization & Interaction
The final data is rendered into an interactive dashboard.
* **Bubble Chart:** Uses `matplotlib` to display keyword frequency, allowing users to spot main themes at a glance.
* **Interactive Transcript:** The segmented text is displayed in blocks, allowing users to read specific sections without scrolling through a wall of text.



## 3. Tech Stack

The project leverages a robust stack of open-source technologies:

* **Programming Language:** Python 3.9+
* **User Interface:** Streamlit (for the web dashboard)
* **Speech-to-Text Model:** OpenAI Whisper (Base/Small/Medium models)
* **Natural Language Processing:** NLTK (TextTiling, Stopwords, Tokenization)
* **Audio Processing:** FFmpeg, Pydub
* **Visualization:** Matplotlib, WordCloud
* **Testing Framework:** Pytest (Unit testing and Mocking)
* **Version Control:** Git & GitHub

## 4. Setup

Follow these steps to set up the project locally:

### Prerequisites

* Python 3.8 or higher installed.
* **FFmpeg** installed and added to your system PATH.
* Git installed.

### Installation

1. **Clone the Repository:**
```bash
git clone <your-github-repo-url>
cd Automated-Podcast-Transcription

```


2. **Create a Virtual Environment:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Download NLTK Data:**
Run this python command once to download necessary NLP packages:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')

```



## 5. Usage

To run the application, execute the following command in your terminal:

```bash
streamlit run src/app.py

```

**How to use the Interface:**

1. Open the local URL provided (usually `http://localhost:8501`).
2. Use the sidebar to upload a podcast file (supported formats: `.wav`, `.mp3`).
3. Click the **"Process Audio"** button.
4. Wait for the pipeline to finish (Transcription -> Segmentation -> Analysis).
5. View the results:
* **Full Transcript:** Read the complete text.
* **Topic Segments:** See the text divided by topic changes.
* **Keyword Analysis:** View the most discussed terms in a bubble chart.



## 6. Testing

The project includes an automated testing suite to ensure reliability.

**Running Tests:**

```bash
python -m pytest

```

* **Scope:** Validates audio preprocessing logic, error handling for missing files, and the accuracy of keyword extraction algorithms.


## 7. Troubleshooting

* **Error: `FileNotFoundError: [WinError 2] The system cannot find the file specified`**
    * **Cause:** FFmpeg is not installed or it is not added to your system PATH.
    * **Fix:** Install FFmpeg, add it to your environment variables, and restart your terminal.

* **App crashes with "Out of Memory"**
    * **Cause:** The Whisper model (defaulting to "medium") is too large for your available RAM.
    * **Fix:** Open `src/transcription.py` and change the line `model_size="medium"` to `model_size="tiny"` or `model_size="base"`.

* **Error: `Streamlit command not found`**
    * **Cause:** The virtual environment is not currently activated.
    * **Fix:** Activate your environment before running the command:
        * **Windows:** `.venv\Scripts\activate`
        * **Mac/Linux:** `source .venv/bin/activate`


### Changes made:

1. **Main Bullets:** Used for the Error messages so they stand out.
2. **Sub-bullets:** Indented "Cause" and "Fix" to keep them organized under the specific error.
3. **Code formatting:** Added backticks ( ``` ) around commands and file paths (like `src/transcription.py`) to make them look like code.


## 8. Limitations and Challenges

* **Processing Speed:** Transcribing long audio files (1 hour+) can take significant time on a CPU. GPU acceleration is recommended for faster performance.
* **Overlapping Speech:** The current model struggles to distinguish individual speakers when multiple people talk at once (Speaker Diarization is not yet implemented).
* **Audio Quality:** Heavy background noise or low-quality recording equipment significantly impacts transcription accuracy.

## 9. Future Scope

* **Speaker Diarization:** Implement pyannote.audio to identify *who* is speaking (e.g., "Speaker A", "Speaker B").
* **Real-Time Transcription:** Adapt the pipeline to transcribe live audio streams rather than just uploaded files.
* **Summarization:** Integrate a Large Language Model (like GPT or BART) to generate a concise 3-paragraph summary of the entire episode.
* **Cloud Deployment:** Deploy the application to AWS or Streamlit Cloud for public access.

## 10. References

1. **OpenAI Whisper:** https://github.com/openai/whisper
2. **Streamlit Documentation:** https://docs.streamlit.io/
3. **NLTK TextTiling:** https://www.nltk.org/api/nltk.tokenize.html
4. **FFmpeg:** https://ffmpeg.org/


