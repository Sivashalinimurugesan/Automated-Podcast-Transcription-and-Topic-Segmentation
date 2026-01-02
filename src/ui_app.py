import streamlit as st
import json
import subprocess
from pathlib import Path
from textblob import TextBlob
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import requests
import re

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
META_FILE = BASE_DIR / "docs" / "processing_metadata.json"
AUDIO_RAW_DIR = BASE_DIR / "audio_raw"

def load_metadata():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return {}

def save_metadata(meta):
    META_FILE.write_text(json.dumps(meta, indent=4))

def load_json(path):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return []

def compute_sentiment(text):
    return round(TextBlob(text).sentiment.polarity, 3)

st.set_page_config(layout="wide", page_title="Podcast Transcription & Segmentation")

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

# Load metadata at the start
metadata = load_metadata()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Dashboard", "Upload & Process", "Transcript View", "Segments & Summaries", "Search & Analysis", "Audio Analysis", "System Info"])

current_title = "Legal ( Automated Podcast Transcription and Topic Segmentation )"
if page == "Dashboard":
    st.title("Dashboard")
    
    # Create metrics
    total_files = len(metadata)
    processed_files = 0
    total_segments = 0
    total_keywords = 0
    
    for key, data in metadata.items():
        if data.get("summarization", {}).get("status") == "done":
            processed_files += 1
            
            # Count segments and keywords if available
            if "segmentation" in data:
                seg_file = Path(data["segmentation"]["segment_file"])
                if seg_file.exists():
                    segments = load_json(seg_file)
                    total_segments += len(segments)
                    
                    for seg in segments:
                        if "keywords" in seg:
                            total_keywords += len(seg["keywords"])
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Files", total_files)
    col2.metric("Processed Files", processed_files)
    col3.metric("Total Segments", total_segments)
    col4.metric("Total Keywords", total_keywords)
    
    st.markdown("## Welcome to the LEGAL Audio Transcription and Topic Segmentation System")
    st.markdown("### This system allows you to upload audio files, transcribe them, segment into topics, and generate summaries.")
    
    st.markdown("### Features:")
    st.markdown("- Audio preprocessing and noise reduction")
    st.markdown("- Automatic speech-to-text transcription")
    st.markdown("- Topic segmentation with boundary detection")
    st.markdown("- Keyword extraction for each segment")
    st.markdown("- AI-powered summarization using Gemini")
    st.markdown("- Interactive visualization and search capabilities")
    
    st.markdown("### How to use:")
    st.markdown("1. Go to 'Upload & Process' to upload your audio file")
    st.markdown("2. Run the processing pipeline")
    st.markdown("3. View transcripts, segments, and summaries")
    st.markdown("4. Search and analyze content")
    
    # Recent files section
    if metadata:
        st.subheader("Recent Files")
        for file_key in list(metadata.keys())[-5:]:  # Show last 5 files
            data = metadata[file_key]
            status = "Processing" if data.get("summarization", {}).get("status") != "done" else "Completed"
            status_icon = "s " if status == "Processing" else "w "
            st.markdown(f"{status_icon} **{file_key}** - {status}")

elif page == "Home":
    st.title(current_title)
    st.markdown("## Welcome to the Automated Podcast Transcription and Topic Segmentation System")
    st.markdown("### This system allows you to upload audio files, transcribe them, segment into topics, and generate summaries.")
    
    st.markdown("### Features:")
    st.markdown("- Audio preprocessing and noise reduction")
    st.markdown("- Automatic speech-to-text transcription")
    st.markdown("- Topic segmentation with boundary detection")
    st.markdown("- Keyword extraction for each segment")
    st.markdown("- AI-powered summarization using Gemini")
    st.markdown("- Interactive visualization and search capabilities")
    
    st.markdown("### How to use:")
    st.markdown("1. Go to 'Upload & Process' to upload your audio file")
    st.markdown("2. Run the processing pipeline")
    st.markdown("3. View transcripts, segments, and summaries")
    st.markdown("4. Search and analyze content")

if page == "Upload & Process":
    st.title("Upload & Process Audio")
    
    # Create tabs for different upload methods
    tab1, tab2 = st.tabs(["Upload File", "Google Drive Link"])
    
    with tab1:
        st.subheader("Upload Audio")
        
        uploaded = st.file_uploader(
            "Upload audio (mp3 / wav / m4a)",
            type=["mp3", "wav", "m4a"]
        )
        
        if uploaded:
            AUDIO_RAW_DIR.mkdir(exist_ok=True)
            audio_path = AUDIO_RAW_DIR / uploaded.name
        
            if audio_path.exists():
                st.warning("File already exists")
            else:
                audio_path.write_bytes(uploaded.read())
                metadata[uploaded.name] = {
                    "preprocessing": {"status": "pending"},
                    "transcription": {"status": "pending"},
                    "segmentation": {"status": "pending"},
                    "keywords": {"status": "pending"},
                    "summarization": {"status": "pending"}
                }
                save_metadata(metadata)
                st.success("Audio uploaded and registered")
    
    with tab2:
        st.subheader("Download from Google Drive")
        
        # Function to extract file ID from Google Drive URL
        def extract_drive_id(url):
            # Pattern for Google Drive URLs
            patterns = [
                r'\/file\/d\/([a-zA-Z0-9-_]+)',
                r'\/open\?id=([a-zA-Z0-9-_]+)',
                r'id=([a-zA-Z0-9-_]+)',
                r'drive\.google\.com\/.*[?&]id=([a-zA-Z0-9-_]+)',
                r'([a-zA-Z0-9-_]{20,})'  # Direct ID
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            return None
        
        def download_from_drive(drive_url, file_path):
            """Download file from Google Drive"""
            file_id = extract_drive_id(drive_url)
            if not file_id:
                st.error("Could not extract file ID from URL")
                return False
            
            # Google Drive download URL
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            try:
                response = requests.get(download_url, stream=True)
                response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return True
            except Exception as e:
                st.error(f"Error downloading file: {str(e)}")
                return False
        
        drive_url = st.text_input("Enter Google Drive shareable link")
        
        if drive_url:
            file_id = extract_drive_id(drive_url)
            if file_id:
                if st.button("Download from Google Drive"):
                    # Try to get the filename from the Drive response
                    # For now, we'll use a temporary name
                    temp_filename = f"drive_file_{file_id}.tmp"
                    temp_path = AUDIO_RAW_DIR / temp_filename
                    
                    if download_from_drive(drive_url, temp_path):
                        # Try to determine the actual file extension by checking the file content
                        import mimetypes
                        import os
                        
                        # Get the actual file type
                        # Try multiple approaches for file type detection
                        
                        # Method 1: Check common audio file headers
                        def detect_audio_format(file_path):
                            with open(file_path, 'rb') as f:
                                header = f.read(12)
                                if header.startswith(b'RIFF') and header[8:12] == b'WAVE':
                                    return '.wav'
                                elif header.startswith(b'ID3') or header.startswith(b'\xFF\xFB'):
                                    return '.mp3'
                                elif header.startswith(b'\xFF\xF9') or header.startswith(b'\xFF\xFA'):
                                    return '.mp3'
                                elif header.startswith(b'\x00\x00\x00') and b'mdat' in header:
                                    return '.m4a'
                                elif header.startswith(b'\x00\x00\x00') and b'ftyp' in header:
                                    # Could be m4a, mp4, etc. Assume m4a for audio
                                    return '.m4a'
                                else:
                                    # Fallback: try to guess from file content
                                    try:
                                        import struct
                                        f.seek(0)
                                        chunk = f.read(20)
                                        # Check for MP3 sync word
                                        if b'\xFF\xFB' in chunk or b'\xFF\xFA' in chunk:
                                            return '.mp3'
                                        # Check for WAV header
                                        if b'RIFF' in chunk and b'WAVE' in chunk:
                                            return '.wav'
                                    except:
                                        pass
                                    return None
                        
                        # Try header detection first
                        ext = detect_audio_format(temp_path)
                        
                        # If header detection failed, try python-magic if available
                        if not ext:
                            try:
                                import magic  # Requires python-magic
                                mime = magic.from_buffer(open(temp_path, 'rb').read(1024), mime=True)
                                ext = mimetypes.guess_extension(mime)
                            except ImportError:
                                # python-magic not available, try to guess from URL
                                if 'mp3' in drive_url.lower():
                                    ext = '.mp3'
                                elif 'wav' in drive_url.lower():
                                    ext = '.wav'
                                elif 'm4a' in drive_url.lower():
                                    ext = '.m4a'
                                else:
                                    ext = None
                        
                        if ext:
                            # Rename the file with correct extension
                            final_filename = f"drive_file_{file_id}{ext}"
                            final_path = AUDIO_RAW_DIR / final_filename
                            os.rename(temp_path, final_path)
                            
                            # Register in metadata
                            metadata[final_filename] = {
                                "preprocessing": {"status": "pending"},
                                "transcription": {"status": "pending"},
                                "segmentation": {"status": "pending"},
                                "keywords": {"status": "pending"},
                                "summarization": {"status": "pending"}
                            }
                            save_metadata(metadata)
                            st.success(f"File downloaded successfully as {final_filename}")
                        else:
                            st.warning("Could not determine file type, keeping as temporary file")
                            # Register the temp file in metadata
                            metadata[temp_filename] = {
                                "preprocessing": {"status": "pending"},
                                "transcription": {"status": "pending"},
                                "segmentation": {"status": "pending"},
                                "keywords": {"status": "pending"},
                                "summarization": {"status": "pending"}
                            }
                            save_metadata(metadata)
                    else:
                        st.error("Failed to download file from Google Drive")
            else:
                st.error("Invalid Google Drive URL")
    
    st.divider()
    
    if not metadata:
        st.error("No audio files available")
        st.stop()
    
    st.subheader("Select Audio")
    file_key = st.selectbox("Available Audio Files", sorted(metadata.keys()))
    data = metadata[file_key]
    
    audio_path = AUDIO_RAW_DIR / file_key
    if not audio_path.exists():
        st.error("Audio file not found")
        st.stop()
    
    st.subheader("Audio Player")
    st.audio(str(audio_path), start_time=st.session_state.start_time)
    
    st.divider()
    
    def run_pipeline():
        # Run preprocessing
        result = subprocess.run(["python", "preprocessing.py"], cwd=SRC_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Preprocessing failed: {result.stderr}")
            return
        
        # Run transcription
        result = subprocess.run(["python", "transcription.py"], cwd=SRC_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Transcription failed: {result.stderr}")
            return
        
        # Run segmentation
        result = subprocess.run(["python", "segmentation.py"], cwd=SRC_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Segmentation failed: {result.stderr}")
            return
        
        # Run keyword extraction
        result = subprocess.run(["python", "keyword_extraction.py"], cwd=SRC_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Keyword extraction failed: {result.stderr}")
            return
        
        # Run summarization
        result = subprocess.run(["python", "summarization.py"], cwd=SRC_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            st.error(f"Summarization failed: {result.stderr}")
            return
        
        st.success("All processing steps completed successfully!")
    
    if data.get("summarization", {}).get("status") != "done":
        if st.button("Run Processing Pipeline (Preprocess, Transcribe, Segment, Keywords, Summarize)"):
            run_pipeline()
            st.rerun()
        st.info("This audio is uploaded but not processed yet")
        st.stop()
    
    st.success("All processing steps completed! You can now view the results in other pages.")

defined_pages = ["Transcript View", "Segments & Summaries", "Search & Analysis", "Audio Analysis", "System Info"]

# Initialize variables to avoid undefined errors
segments = []
data = {}
file_key = None
all_keywords = []

if page in defined_pages and metadata:
    st.title(page)
    
    file_key = st.selectbox("Select Audio File", sorted(metadata.keys()))
    data = metadata[file_key]
    
    audio_path = AUDIO_RAW_DIR / file_key
    if not audio_path.exists():
        st.error("Audio file not found")
        st.stop()
    
    # Check if the file has been processed
    required_processing = ["preprocessing", "transcription", "segmentation", "keywords", "summarization"]
    all_processed = all(data.get(proc, {}).get("status") == "done" for proc in required_processing)
    
    if not all_processed:
        st.warning("This audio file has not been fully processed yet. Please go to 'Upload & Process' page first.")
        # Show which steps are still pending
        for proc in required_processing:
            status = data.get(proc, {}).get("status", "not started")
            if status != "done":
                st.info(f"{proc.title()}: {status}")
        st.stop()
    
    segments = load_json(data["segmentation"]["segment_file"])
    if not segments:
        st.warning("No segments available")
        st.stop()
    
    for s in segments:
        s.setdefault("sentiment", compute_sentiment(s.get("text", "")))
    
    # Define all_keywords after segments are loaded
    all_keywords = []
    for s in segments:
        all_keywords.extend(s.get("keywords", []))

if page == "Transcript View":
    st.subheader("Full Transcript")
    
    # Get transcript path from metadata
    transcript_path = Path(data["transcription"]["transcript_file"])
    if transcript_path.exists():
        with st.expander("View Full Transcript", expanded=True):
            full_text = transcript_path.read_text().strip()
            for para in full_text.split("\n\n"):
                if para.strip():
                    st.write(para.strip())
    
    if data.get("summarization", {}).get("status") == "done":
        st.subheader("Full Transcript Summary")
        # Generate summary of full transcript
        try:
            from summarization import summarize_full_transcript
            full_text = transcript_path.read_text().strip()
            full_summary = summarize_full_transcript(full_text)
            st.info(full_summary)
        except ImportError:
            st.warning("Summarization module not available")

if page == "Segments & Summaries":
    st.subheader("Segmented Content with Summaries")
    
    for idx, seg in enumerate(segments, start=1):
        with st.expander(f"Segment {idx}: {seg['start']:.2f}s - {seg['end']:.2f}s", expanded=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Transcript:**")
                st.write(seg["text"])
                
                if seg.get("summary"):
                    st.markdown("**Summary:**")
                    st.success(seg["summary"])
                
                if seg.get("keywords"):
                    st.caption("**Keywords:** " + ", ".join(seg["keywords"]))
                
                st.caption(f"**Sentiment:** {seg['sentiment']}")
            
            with col2:
                st.markdown(f"**Start:** {seg['start']:.2f}s")
                st.markdown(f"**End:** {seg['end']:.2f}s")
                st.markdown(f"**Duration:** {seg['end'] - seg['start']:.2f}s")
                
                if st.button(f"Play Segment", key=f"play_{idx}"):
                    st.session_state.start_time = int(seg["start"])
                    st.rerun()

if page == "Search & Analysis":
    st.subheader("Search & Analysis")
    
    all_keywords = []
    for s in segments:
        all_keywords.extend(s.get("keywords", []))
    
    st.subheader("Sentiment Timeline")
    
    timeline_df = {
        "Start (sec)": [s["start"] for s in segments],
        "Sentiment": [s["sentiment"] for s in segments],
        "Preview": [s["text"][:120] for s in segments]
    }
    
    timeline_fig = px.scatter(
        timeline_df,
        x="Start (sec)",
        y="Sentiment",
        hover_data=["Preview"],
        height=350
    )
    
    st.plotly_chart(timeline_fig, width='stretch')
    
    st.divider()
    
    st.subheader("Keyword Cloud")
    
    if all_keywords:
        wc = WordCloud(width=900, height=300, background_color="white")
        wc.generate_from_frequencies(Counter(all_keywords))
        st.image(wc.to_image(), width='stretch')
    
    st.divider()
    
    st.subheader("Search Transcript")
    
    c1, c2 = st.columns([2, 3])
    with c1:
        selected_keyword = st.selectbox("Select keyword", ["None"] + sorted(set(all_keywords)))
    with c2:
        typed_keyword = st.text_input("Type keyword or text")
    
    st.divider()
    
    filtered = []
    
    for seg in segments:
        text = seg["text"]
        keywords = seg.get("keywords", [])
    
        if typed_keyword:
            if typed_keyword.lower() in text.lower() or any(
                typed_keyword.lower() in k.lower() for k in keywords
            ):
                filtered.append(seg)
        elif selected_keyword != "None":
            if selected_keyword in keywords:
                filtered.append(seg)
    
    st.subheader("Search Results")
    
    if not filtered:
        st.info("Select or type a keyword to view transcript")
    else:
        for idx, seg in enumerate(filtered, start=1):
            c1, c2 = st.columns([1, 6])
    
            with c1:
                st.markdown(f"{seg['start']:.2f}s")
                if st.button("Play", key=f"play_search_{idx}"):
                    st.session_state.start_time = int(seg["start"])
                    st.rerun()
    
            with c2:
                st.markdown(seg["text"])
                if seg.get("summary"):
                    st.success(f"**Summary:** {seg['summary']}")
                if seg.get("keywords"):
                    st.caption("Keywords: " + ", ".join(seg["keywords"]))
                st.caption(f"Sentiment: {seg['sentiment']}")
    
            st.divider()



if page == "Audio Analysis":
    st.subheader("Audio Analysis")
    
    # Display audio statistics
    st.markdown(f"**Audio Duration:** {data.get('transcription', {}).get('audio_duration_sec', 'N/A')} seconds")
    st.markdown(f"**Transcript Length:** {len(segments)} segments")
    st.markdown(f"**Total Keywords Extracted:** {len(all_keywords)}")
    
    # Sentiment analysis
    sentiments = [s["sentiment"] for s in segments]
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    st.markdown(f"**Average Sentiment:** {avg_sentiment:.2f}")
    
    # Show sentiment distribution
    st.subheader("Sentiment Distribution")
    sentiment_counts = {
        "Positive": len([s for s in sentiments if s > 0.1]),
        "Neutral": len([s for s in sentiments if -0.1 <= s <= 0.1]),
        "Negative": len([s for s in sentiments if s < -0.1])
    }
    
    import pandas as pd
    sentiment_df = pd.DataFrame(list(sentiment_counts.items()), columns=['Sentiment', 'Count'])
    st.bar_chart(sentiment_df.set_index('Sentiment'))
    
    # Segment duration analysis
    st.subheader("Segment Duration Analysis")
    durations = [s['end'] - s['start'] for s in segments]
    duration_df = pd.DataFrame({
        'Segment': [f'Seg {i+1}' for i in range(len(durations))],
        'Duration': durations
    })
    st.line_chart(duration_df.set_index('Segment'))

if page == "System Info":
    st.subheader("System Information")
    
    st.markdown("### Processing Pipeline Status")
    preprocessing_status = data.get('preprocessing', {}).get('status', 'Not started')
    transcription_status = data.get('transcription', {}).get('status', 'Not started')
    segmentation_status = data.get('segmentation', {}).get('status', 'Not started')
    keywords_status = data.get('keywords', {}).get('status', 'Not started')
    summarization_status = data.get('summarization', {}).get('status', 'Not started')
    
    status_mapping = {
        'done': '',
        'pending': '',
        'Not started': ''
    }
    
    st.markdown(f"{status_mapping.get(preprocessing_status, '❓')} **Preprocessing:** {preprocessing_status}")
    st.markdown(f"{status_mapping.get(transcription_status, '❓')} **Transcription:** {transcription_status}")
    st.markdown(f"{status_mapping.get(segmentation_status, '❓')} **Segmentation:** {segmentation_status}")
    st.markdown(f"{status_mapping.get(keywords_status, '❓')} **Keyword Extraction:** {keywords_status}")
    st.markdown(f"{status_mapping.get(summarization_status, '❓')} **Summarization:** {summarization_status}")
    
    st.markdown("### Processing Details")
    if 'transcription' in data:
        st.markdown(f"**Engine:** {data['transcription'].get('engine', 'N/A')}")
        st.markdown(f"**Chunks:** {data['transcription'].get('total_chunks', 'N/A')}")
        st.markdown(f"**Time Taken:** {data['transcription'].get('time_taken_sec', 'N/A')} seconds")
    
    if 'segmentation' in data:
        st.markdown(f"**Model:** {data['segmentation'].get('model', 'N/A')}")
        st.markdown(f"**Total Segments:** {data['segmentation'].get('total_segments', 'N/A')}")
    
    if 'summarization' in data:
        st.markdown(f"**Engine:** {data['summarization'].get('engine', 'N/A')}")
    
    st.markdown("### System Configuration")
    import os
    st.markdown(f"**Python Version:** {os.sys.version}")
    st.markdown(f"**Working Directory:** {os.getcwd()}")
    
    # Show available audio files
    st.markdown("### Available Audio Files")
    audio_files = [f for f in os.listdir(AUDIO_RAW_DIR) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
    for audio_file in audio_files:
        st.markdown(f"- {audio_file}")


