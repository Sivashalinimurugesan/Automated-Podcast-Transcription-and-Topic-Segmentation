import unittest
import tempfile
import json
import os
from pathlib import Path
import shutil


class TestProcessingPipeline(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dirs = {
            'audio_raw': 'audio_raw',
            'audio_processed': 'audio_processed', 
            'transcripts': 'transcripts',
            'segments': 'segments',
            'docs': 'docs'
        }
        
        # Create temporary directories
        for dir_name, original_path in self.original_dirs.items():
            temp_path = Path(self.test_dir) / dir_name
            temp_path.mkdir(exist_ok=True)
            setattr(self, f'temp_{dir_name}', temp_path)
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        shutil.rmtree(self.test_dir)
    
    def test_full_pipeline_integration(self):
        """Test the integration of all components in the processing pipeline."""
        # Create test metadata
        test_metadata = {
            "test_audio.wav": {
                "preprocessing": {"status": "done", "processed_audio": str(self.temp_audio_processed / "test_audio_denoised.wav")},
                "transcription": {"status": "done", "transcript_file": str(self.temp_transcripts / "test_audio_transcript.txt")},
                "segmentation": {"status": "done", "segment_file": str(self.temp_segments / "test_audio_segments.json")},
                "keywords": {"status": "done"},
                "summarization": {"status": "pending"}  # We'll test this part
            }
        }
        
        # Create test segments file
        test_segments = [
            {
                "start": 0.0,
                "end": 10.0,
                "text": "This is a test segment about machine learning and AI. It covers various aspects.",
                "keywords": ["machine learning", "AI", "aspects"]
            },
            {
                "start": 10.0,
                "end": 20.0, 
                "text": "This is another segment about data science and analytics. It has different content.",
                "keywords": ["data science", "analytics", "content"]
            }
        ]
        
        # Write test segments file
        test_segments_path = self.temp_segments / "test_audio_segments.json"
        test_segments_path.write_text(json.dumps(test_segments))
        
        # Temporarily modify environment variables for testing
        import os
        original_env = {}
        for key, value in self.original_dirs.items():
            env_key = key.upper().replace('_', '').replace('audio', 'AUDIO_').upper()
            if env_key == 'DOCS':
                env_key = 'DOCS_DIR'
            elif env_key == 'AUDIO_RAW':
                env_key = 'AUDIO_RAW_DIR'
            elif env_key == 'AUDIO_PROCESSED':
                env_key = 'AUDIO_PROCESSED_DIR'
            elif env_key == 'TRANSCRIPTS':
                env_key = 'TRANSCRIPTS_DIR'
            elif env_key == 'SEGMENTS':
                env_key = 'SEGMENTS_DIR'
            
            original_env[env_key] = os.environ.get(env_key)
            os.environ[env_key] = str(getattr(self, f'temp_{key}'))
        
        # Temporarily modify the metadata file location
        from src.summarization import META_FILE as SUMMARIZATION_META_FILE
        from src.segmentation import META_FILE as SEGMENTATION_META_FILE
        from src.keyword_extraction import META_FILE as KEYWORD_META_FILE
        from src.transcription import META_FILE as TRANSCRIPTION_META_FILE
        from src.preprocessing import META_FILE as PREPROCESSING_META_FILE
        
        # Update all modules to use test metadata file
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        
        # Import modules to modify their META_FILE variables
        import preprocessing
        import transcription
        import segmentation
        import keyword_extraction
        import summarization
        
        # Set all modules to use the same test metadata file
        test_meta_file = self.temp_docs / "processing_metadata.json"
        test_meta_file.write_text(json.dumps(test_metadata))
        
        preprocessing.META_FILE = str(test_meta_file)
        transcription.META_FILE = str(test_meta_file)
        segmentation.META_FILE = str(test_meta_file)
        keyword_extraction.META_FILE = str(test_meta_file)
        summarization.META_FILE = str(test_meta_file)
        
        try:
            # Test that all modules can be imported and run
            from src.preprocessing import process_all_audio
            from src.transcription import process_all_transcriptions
            from src.segmentation import run_segmentation
            from src.keyword_extraction import run_keywords
            from src.summarization import run_summarization
            
            # Run the summarization part of the pipeline
            run_summarization()
            
            # Verify that summaries were added to the segments
            updated_segments = json.loads(test_segments_path.read_text())
            for segment in updated_segments:
                self.assertIn("summary", segment)
                self.assertIsInstance(segment["summary"], str)
                
        finally:
            # Restore original environment variables
            for key, value in original_env.items():
                if value is not None:
                    os.environ[key] = value
                else:
                    os.environ.pop(key, None)
    
    def test_pipeline_status_tracking(self):
        """Test that the pipeline properly tracks processing status."""
        # Create test metadata with various statuses
        test_metadata = {
            "test_file.wav": {
                "preprocessing": {"status": "done"},
                "transcription": {"status": "pending"},
                "segmentation": {"status": "pending"},
                "keywords": {"status": "pending"},
                "summarization": {"status": "pending"}
            }
        }
        
        # Write test metadata
        test_meta_file = self.temp_docs / "processing_metadata.json"
        test_meta_file.write_text(json.dumps(test_metadata))
        
        # Verify we can load the metadata correctly
        from src.ui_app import load_metadata
        loaded_metadata = load_metadata()
        
        self.assertEqual(loaded_metadata["test_file.wav"]["preprocessing"]["status"], "done")
        self.assertEqual(loaded_metadata["test_file.wav"]["transcription"]["status"], "pending")


if __name__ == '__main__':
    print("Running pipeline integration tests...")
    unittest.main()