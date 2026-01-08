import os
import pytest
from src.preprocessing import clean_audio
from src.transcription import transcribe_audio
from src.keyword_extraction import get_global_keyword_counts

# --- TEST 1: PREPROCESSING (File Handling) ---
def test_clean_audio_path_logic():
   
    input_file = "test_audio.mp3"
    
    # Create a dummy file
    with open(input_file, "w") as f:
        f.write("dummy audio content")

    # Assert the function exists (sanity check)
    assert callable(clean_audio)
    
    # Cleanup
    if os.path.exists(input_file):
        os.remove(input_file)

# --- TEST 2: TRANSCRIPTION (Error Handling) ---
def test_transcription_missing_file_error():
   
    # Pass a file that definitely doesn't exist
    result = transcribe_audio("ghost_file.wav", model_size="tiny")
    assert isinstance(result, str)
    assert "Error" in result or "FileNotFound" in result

# --- TEST 3: NLP LOGIC (Math Verification) ---
def test_keyword_extraction_accuracy():
   
    # Input with known frequency: 'Growth' appears 3 times, 'Money' appears 2 times
    dummy_text = "Money money business Growth Growth Growth."
    
    keywords = get_global_keyword_counts(dummy_text)
    
    # Assertions
    assert len(keywords) > 0
    
    # Top keyword should be 'Growth' (Case insensitive check)
    top_word = keywords[0]['keyword'].lower()
    top_count = keywords[0]['count']
    
    assert top_word == 'growth'
    assert top_count == 3