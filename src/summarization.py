import json
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
META_FILE = PROJECT_ROOT / "docs" / "processing_metadata.json"

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

# Get max sentences from environment variable
MAX_SENTENCES = int(os.getenv("SUMMARY_MAX_SENTENCES", 3))

# Configure the model
model = genai.GenerativeModel('gemini-pro')


def generate_summary(text, max_sentences=None):
    """
    Generate a summary for the given text using Gemini API
    
    Args:
        text (str): The text to summarize
        max_sentences (int): Maximum number of sentences in the summary. If None, uses env var
    
    Returns:
        str: Generated summary
    """
    if not text.strip():
        return ""
    
    if max_sentences is None:
        max_sentences = MAX_SENTENCES

    prompt = f"""Please provide a concise summary of the following text in {max_sentences} sentences or fewer. 
    Focus on the main points and key information:
    
    {text}
    
    Summary:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary generation failed"


def run_summarization():
    """
    Run summarization on all segments in the metadata
    """
    if not META_FILE.exists():
        raise RuntimeError("processing_metadata.json not found")

    metadata = json.loads(META_FILE.read_text())

    for key, data in metadata.items():
        if "segmentation" not in data:
            continue

        seg_file = Path(data["segmentation"]["segment_file"])
        if not seg_file.exists():
            continue

        segments = json.loads(seg_file.read_text())
        if not segments:
            continue

        # Generate summaries for each segment
        for seg in segments:
            if "text" not in seg or not seg["text"].strip():
                seg["summary"] = ""
            else:
                seg["summary"] = generate_summary(seg["text"])

        # Write updated segments back to file
        seg_file.write_text(json.dumps(segments, indent=4))

        # Update metadata to indicate summarization is done
        data["summarization"] = {
            "engine": "gemini-pro",
            "total_segments": len(segments),
            "status": "done"
        }

    # Save updated metadata
    META_FILE.write_text(json.dumps(metadata, indent=4))


def summarize_full_transcript(transcript_text):
    """
    Generate a summary for the entire transcript
    
    Args:
        transcript_text (str): Full transcript text
    
    Returns:
        str: Summary of the entire transcript
    """
    # Use 5 sentences for full transcript summary, regardless of env var
    return generate_summary(transcript_text, max_sentences=5)


if __name__ == "__main__":
    run_summarization()
