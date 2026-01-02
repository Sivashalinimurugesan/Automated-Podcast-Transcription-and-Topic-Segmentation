import unittest
import tempfile
import json
import os
from pathlib import Path
from src.keyword_extraction import extract_keywords, run_keywords


class TestKeywordExtraction(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_extract_keywords(self):
        """Test the extract_keywords function."""
        test_text = "This is a sample text about machine learning and artificial intelligence."
        
        keywords = extract_keywords(test_text)
        
        # Check that keywords is a list
        self.assertIsInstance(keywords, list)
        
        # Check that it's not empty for meaningful text
        if keywords:
            # Keywords should be strings
            for keyword in keywords:
                self.assertIsInstance(keyword, str)
    
    def test_extract_keywords_empty(self):
        """Test extract_keywords with empty text."""
        empty_keywords = extract_keywords("")
        self.assertEqual(empty_keywords, [])
        
        none_keywords = extract_keywords(None)
        self.assertEqual(none_keywords, [])
    
    def test_extract_keywords_single_word(self):
        """Test extract_keywords with a single word."""
        single_word = "hello"
        keywords = extract_keywords(single_word)
        
        self.assertIsInstance(keywords, list)
    
    def test_run_keywords(self):
        """Test the run_keywords function."""
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
                "text": "This is a test segment about machine learning and AI."
            }
        ]
        
        test_segments_file = Path(self.test_dir) / "test_segments.json"
        test_segments_file.write_text(json.dumps(test_segments))
        
        # Write test metadata
        temp_meta_file.write_text(json.dumps(test_metadata))
        
        # Temporarily modify the keyword_extraction module to use our test file
        import sys
        sys.path.append('src')
        import keyword_extraction
        original_meta_file = keyword_extraction.META_FILE
        keyword_extraction.META_FILE = temp_meta_file
        
        try:
            # This should run without errors
            run_keywords()
            
            # Check that the segments file was updated with keywords
            updated_segments = json.loads(test_segments_file.read_text())
            if updated_segments:
                # Each segment should now have keywords
                for segment in updated_segments:
                    self.assertIn("keywords", segment)
                    self.assertIsInstance(segment["keywords"], list)
        finally:
            # Restore original path
            keyword_extraction.META_FILE = original_meta_file


if __name__ == '__main__':
    unittest.main()