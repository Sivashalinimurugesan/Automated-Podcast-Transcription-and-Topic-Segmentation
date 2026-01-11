# Project Documentation

## 1. Title

**Automated Podcast Transcription and Topic Segmentation Platform**

## 2. Overview

This project is an AI-powered web application designed to process long-form audio content, such as podcasts or lectures. The system automatically transcribes audio into text, segments the content into distinct logical topics, and performs sentiment analysis on each segment. It solves the problem of navigating long audio files by providing a searchable, visual, and interactive dashboard, allowing users to quickly identify and jump to key moments without listening to the entire recording.

## 3. Approach

The solution follows a modular "Upload-Process-Visualize" workflow:

1. **Ingestion:** The user uploads an audio file (`.mp3` or `.wav`) via the React frontend.
2. **Preprocessing:** The Python backend receives the file, validates the format, and uses `Librosa`/`Pydub` to calculate duration and prepare the audio for processing.
3. **AI Analysis:**
* **Transcription:** The audio is converted to text using an automated speech-to-text model.
* **Segmentation:** The text is analyzed using Natural Language Processing (NLP) techniques (TF-IDF vectorization and clustering) to detect topic shifts and break the transcript into logical segments.
* **Sentiment Analysis:** Each segment is analyzed using VADER (Valence Aware Dictionary and sEntiment Reasoner) to determine the emotional tone (Positive, Negative, or Neutral).


4. **Visualization:** The processed data is sent back to the frontend, where it is rendered into an interactive dashboard featuring audio playback sync, sentiment graphs, and topic summaries.

## 4. Tech Stack

**Frontend (User Interface):**

* **React.js (Vite):** Core framework for building a fast, responsive single-page application.
* **Recharts:** Library used for rendering the interactive Sentiment Timeline and Distribution graphs.
* **CSS Modules:** For component-scoped styling and responsive design.

**Backend (Server & AI Processing):**

* **Python (Flask):** RESTful API server to handle requests and manage data flow.
* **Scikit-learn:** Used for TF-IDF vectorization and text clustering algorithms for segmentation.
* **VADER Sentiment:** Rule-based sentiment analysis tool optimized for social media and conversation texts.
* **Pydub / Librosa:** Audio processing libraries for file manipulation and metadata extraction.

## 5. Setup

Follow these steps to deploy the project locally:

**Prerequisites:**

* Python 3.9+
* Node.js & npm

**Installation:**

1. **Clone Repository:**
```bash
git clone <repository_url>
cd Automated-Podcast-Transcription-and-Topic-Segmentation

```


2. **Backend Configuration:**
```bash
cd Automated-Podcast-Transcription-and-Topic-Segmentation
cd src\backend
pip install -r requirements.txt
python server.py

```


*Server runs on: `http://127.0.0.1:5000*`
3. **Frontend Configuration:**
```bash
cd Automated-Podcast-Transcription-and-Topic-Segmentation
cd src\frontend
npm install
npm run dev

```


*Client runs on: `http://localhost:5173*`

## 6. Testing & Validation

This project includes a modular **Unit Testing Suite** to ensure backend reliability. The tests cover API health checks, file validation, and error handling.

### **How to Run Tests**
1. Navigate to the backend directory:
   ```bash
   cd src/backend
   Run the Automated Test Suite:python -m unittest discover tests

## 7. Usage

1. **Upload:** Open the application in your browser. Drag and drop an `.mp3` or `.wav` file into the upload area or click "Select File".
2. **Processing:** Click the "Start AI Process" button. A loading indicator will appear while the backend analyzes the audio.
3. **Dashboard:** Once complete, the dashboard will populate with:
* **Segment List:** Click any segment on the left to read its summary.
* **Audio Player:** The player automatically syncs to the start time of the selected segment.
* **Visualization:** View the "Sentiment" tab to see the emotional timeline graph.


4. **Search:** Use the "Search" tab to find specific keywords across all segments.

## 8. Troubleshooting

* **"Backend Offline" Error:** Ensure the Python server is running in a separate terminal window and that port 5000 is free.
* **Upload Fails:** Check that the file is strictly `.mp3` or `.wav` format. The system blocks other file types (like PDF) for security.
* **Empty Graphs:** If the graph is blank, ensure the audio file has distinct speech content. Silence or music-only files may result in neutral scores (0.0).

## 9. Limitations and Challenges

* **Processing Time:** Analyzing long audio files (1+ hours) can take significant time (1-2 minutes) depending on CPU power.
* **Context Nuance:** The VADER sentiment model is lexicon-based and may struggle to detect sarcasm or complex cultural nuances compared to advanced transformer models (like BERT).
* **Speaker Identification:** The current version segments by *topic*, but does not distinguish between different *speakers* (Diarization).

## 10. Future Scope

* **Speaker Diarization:** Implementing models (like PyAnnotate) to label "Speaker A" and "Speaker B" in the transcript.
* **User Authentication:** Adding a login system (Firebase/Auth0) so users can save their analysis history and access it later.
* **Export Functionality:** Allowing users to download the analysis report as a PDF or formatted Word document.
* **Real-time Processing:** Exploring streaming transcription for live audio feeds.

## 11. References

1. **React Documentation:** [https://react.dev/](https://react.dev/)
2. **Flask Documentation:** [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
3. **Recharts Library:** [https://recharts.org/](https://recharts.org/)
4. **VADER Sentiment Analysis Paper:** Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text.
5. **Scikit-learn Documentation:** [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/) (For TF-IDF and Clustering algorithms).