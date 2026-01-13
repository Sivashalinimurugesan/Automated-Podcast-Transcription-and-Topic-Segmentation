# Automated Medical Podcast Transcription and Topic Segmentation

## Project Overview

Medical podcasts contain valuable discussions on diseases, treatments, research findings, and clinical experiences. However, these podcasts are often long and difficult to navigate.

This project builds an AI-powered system that automatically transcribes medical podcast audio, detects topic boundaries, and segments the content into meaningful medical topics with summaries, keywords, sentiment analysis, and quality evaluation.

The system enables students, researchers, and healthcare professionals to quickly access relevant medical information without listening to the entire podcast episode.

---

## Use Case (Medical Domain)

This system is designed specifically for medical podcasts, including:

- Clinical discussions  
- Disease awareness talks  
- Medical education podcasts  
- Expert interviews and panel discussions  
- Public health awareness programs  

### Benefits

- Quickly locate discussions about specific diseases or symptoms  
- Navigate podcasts using topic-wise segmentation  
- Understand content through summaries, keywords, sentiment, and quality metrics  
- Save time for medical students and professionals  

---

## Project Objectives

### 1. Transcription (Speech-to-Text)
- Convert long medical podcast audio into text using ASR models  
- Handle noisy, real-world medical audio  
- Generate timestamps for each transcribed segment  

### 2. Topic Segmentation
- Detect topic shifts in medical discussions  
- Segment transcripts into meaningful medical chapters  
- Apply NLP techniques such as:
  - TextTiling  
  - Embedding similarity (Sentence Transformers / BERT)  
  - Change-point detection  

### 3. Summarization and Keyword Extraction
- Generate concise summaries for each segment  
- Extract domain-relevant medical keywords  
- Generate keyword frequency visualizations  

### 4. Sentiment and Quality Analysis
- Perform sentiment analysis on segmented topics  
- Normalize sentiment for medical-domain context  
- Compute transcription quality metrics:
  - Word Error Rate (WER)  
  - Character Error Rate (CER)  
  - Semantic similarity using Sentence Transformers  
- Produce a normalized quality score for UI display  

### 5. Frontend UI for Navigation
- Topic-wise transcript visualization  
- Timestamp-based audio playback  
- Keyword cloud visualization  
- Sentiment and quality dashboards  
- Interactive UI integrated with backend APIs  

---

## System Architecture

Audio Input  
↓  
Audio Preprocessing  
↓  
Medical Speech-to-Text (ASR)  
↓  
Transcript Cleaning & Normalization  
↓  
Embedding Model  
↓  
Topic Segmentation  
↓  
Medical Summaries, Keywords & Sentiment  
↓  
Quality Evaluation (WER, CER, Similarity)  
↓  
Indexing  
↓  
Frontend UI (Search, Playback, Visualization)

---

## Tech Stack

### Backend
- Python 3.9+  
- Flask  
- Whisper (OpenAI) / Faster-Whisper  
- Librosa, PyDub, FFmpeg  

### NLP and Machine Learning
- NLTK  
- SpaCy  
- HuggingFace Transformers  
- Sentence Transformers  
- KeyBERT / YAKE / RAKE  

### Frontend
- React.js  
- HTML, CSS, JavaScript  
- REST API integration  

### Visualization
- Chart.js  
- Plotly  
- Matplotlib  

### Storage
- JSON / CSV  
- SQLite (optional)  
- FAISS / Vector Database (optional)  

---

## Project Structure

```text
Automated-Podcast-Transcription-and-Topic-Segmentation/
│
├── src/
│   ├── preprocessing.py
│   ├── transcription.py
│   ├── segmentation.py
│   ├── evaluation_summary.py
│   ├── evaluation.py
│   ├── keyword_cloud.py
│   ├── keywords.py
│   ├── sentiment.py
│   ├── pipeline_controller.py
│   ├── user_state_manager.py
│   └── logger.py
│
├── ui_app/
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── KeywordCloudView.jsx
│       │   ├── QualityDashboard.jsx
│       │   └── SegmentSentiment.jsx
│       ├── App.js
│       └── index.js
│
├── Inference/
│   ├── transcripts/
│   ├── segments/
│   └── keywords/
│
├── test/
│   ├── conftest.py
│   ├── test_evaluation.py
│   ├── test_keywords.py
│   ├── test_logger.py
│   ├── test_segmentation.py
│   └── test_sentiment.py
│
├── pytest.ini
├── README.md
├── requirements.txt
└── .env.example
```
## Usage

Follow the steps below to set up and run the Automated Medical Podcast Transcription and Topic Segmentation application locally.

### Prerequisites
- Python 3.9 or higher
- Node.js 16+ (for frontend UI)
- Git
- FFmpeg (required for audio processing)

---

### 1. Clone the Repository

git clone https://github.com/springboardmentor13579x-proj/Automated-Podcast-Transcription-and-Topic-Segmentation.git  
cd Automated-Podcast-Transcription-and-Topic-Segmentation

---

### 2. Create and Activate Virtual Environment (Recommended)

python -m venv venv

Windows:  
venv\Scripts\activate

Linux / macOS:  
source venv/bin/activate

---

### 3. Install Backend Dependencies

pip install -r requirements.txt

---

### 4. Configure Environment Variables

Create a .env file using the provided example:

cp .env.example .env

Update required API keys or configuration values inside the .env file.

---

### 5. Run the Backend Application

Start the Flask backend server:

python app.py

The backend initializes audio preprocessing, transcription, topic segmentation, keyword extraction, sentiment analysis, and quality evaluation modules.

---

### 6. Run the Frontend UI (Optional)

Navigate to the frontend directory:

cd ui_app  
npm install  
npm start

The application UI will be available at:

http://localhost:3000

---

### 7. Output and Results

- Generated transcripts, topic segments, keywords, sentiment scores, and quality metrics are stored in the Inference/ directory.
- Outputs are saved in structured formats such as JSON and CSV for further analysis and visualization.

---

### UI Preview


![UI Landing Page](docs/Screenshot%202026-01-12%20183624.png)

---


## Testing and Validation 

Comprehensive **Pytest-based unit testing** has been added to validate the reliability and correctness of the backend modules without altering the core application logic.

### Test Coverage

Unit tests have been implemented for the following backend components:

- **Sentiment Analysis**
  - Validates output structure and sentiment score range
- **Keyword Extraction & Visualization**
  - Ensures keyword processing works correctly
  - Verifies keyword cloud image generation
- **Topic Segmentation**
  - Confirms segmentation output structure for UI compatibility
- **Logger Module**
  - Verifies logger creation and configuration
- **Quality Evaluation**
  - Tests WER, CER, semantic similarity, and normalized quality score computation

### Testing Guarantees

- All unit tests **pass successfully**
- Core business logic remains **unchanged**
- Outputs are **UI-safe and test-safe**
- Edge cases such as empty inputs and invalid data are handled gracefully

### Running Tests

To execute all tests locally:

```bash
pytest -v
```
---

## Milestone-wise Implementation

### Milestone 1: Audio Preprocessing & Transcription
- Audio normalization  
- ASR-based transcription  

### Milestone 2: Topic Segmentation & Keyword Extraction
- Topic boundary detection  
- Medical keyword extraction  

### Milestone 3: Sentiment & Quality Evaluation
- Segment-level sentiment analysis  
- WER, CER, and semantic similarity computation  

### Milestone 4: Frontend Integration & Visualization
- React-based UI  
- Topic navigation and playback  
- Keyword, sentiment, and quality dashboards  

### Milestone 5: Documentation & Final Delivery
- Technical documentation  
- Final demo and evaluation  

---

## Data and Privacy Considerations
- Raw audio and large files are not committed to the repository  
- API keys are managed using environment variables  
- Only source code and configuration files are version-controlled  

---

## Future Enhancements
- Medical entity recognition (NER)  
- Speaker diarization  
- Semantic search across episodes  
- Multi-language support  

---

## Intended Users
- Medical students  
- Healthcare professionals  
- Researchers  
- Medical educators  

---

## License
This project is licensed under the **MIT License**.
