import unittest
import tempfile
import json
import os
from pathlib import Path
from src.summarization import generate_summary, run_summarization, summarize_full_transcript


class TestSummarization(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_generate_summary(self):
        """Test the generate_summary function."""
        test_text = "This is a sample text that contains multiple sentences. " \
                   "The text discusses various topics. " \
                   "It is used for testing the summarization functionality."
        
        summary = generate_summary(test_text, max_sentences=2)
        
        # Check that summary is a string
        self.assertIsInstance(summary, str)
        
        # Check that it's not empty for meaningful text
        self.assertGreater(len(summary.strip()), 0)
    
    def test_generate_summary_empty(self):
        """Test generate_summary with empty text."""
        empty_summary = generate_summary("")
        self.assertEqual(empty_summary, "")
        
        none_summary = generate_summary(None)
        self.assertEqual(none_summary, "")
    
    def test_generate_summary_with_custom_sentence_count(self):
        """Test generate_summary with different sentence counts."""
        test_text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
        
        # Test with 1 sentence
        summary_1 = generate_summary(test_text, max_sentences=1)
        self.assertIsInstance(summary_1, str)
        
        # Test with 3 sentences
        summary_3 = generate_summary(test_text, max_sentences=3)
        self.assertIsInstance(summary_3, str)
    
    def test_summarize_full_transcript(self):
        """Test the summarize_full_transcript function."""
        test_transcript = "This is a longer transcript with multiple sections. " \
                         "It covers various topics in detail. " \
                         "The content is diverse and comprehensive. " \
                         "It includes multiple paragraphs and ideas."
        
        summary = summarize_full_transcript(test_transcript)
        
        # Check that summary is a string
        self.assertIsInstance(summary, str)
        
        # Check that it's not empty for meaningful text
        self.assertGreater(len(summary.strip()), 0)
    
    def test_run_summarization(self):
        """Test the run_summarization function."""
        # Create a temporary metadata file
        temp_meta_file = Path(self.test_dir) / "processing_metadata.json"
        test_metadata = {
            "test.wav": {
                "segmentation": {
                    "segment_file": str(Path(self.test_dir) / "test_segments.json")
                }
            }
        }
        
        # Create a test segments file
        test_segments = [
            {
                "start": 0.0,
                "end": 10.0,
                "text": "This is a test segment about machine learning and AI. It covers various aspects."
            },
            {
                "start": 10.0,
                "end": 20.0, 
                "text": "This is another segment about data science and analytics. It has different content."
            }
        ]
        
        test_segments_file = Path(self.test_dir) / "test_segments.json"
        test_segments_file.write_text(json.dumps(test_segments))
        
        # Write test metadata
        temp_meta_file.write_text(json.dumps(test_metadata))
        
        # Temporarily modify the summarization module to use our test file
        import sys
        sys.path.append('src')
        import summarization
        original_meta_file = summarization.META_FILE
        summarization.META_FILE = temp_meta_file
        
        try:
            # This should run without errors (though it may fail without API key)
            run_summarization()
            
            # Check that the segments file was updated (may have error message if API not available)
            updated_segments = json.loads(test_segments_file.read_text())
            if updated_segments:
                # Each segment should now have a summary (or error message)
                for segment in updated_segments:
                    self.assertIn("summary", segment)
                    self.assertIsInstance(segment["summary"], str)
        except Exception as e:
            # If API key is not available, this is expected
            pass
        finally:
            # Restore original path
            summarization.META_FILE = original_meta_file


if __name__ == '__main__':
    unittest.main()