import unittest
import tempfile
import json
import os
from pathlib import Path
from src.segmentation import segment_text, load_metadata


class TestSegmentation(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_segment_text(self):
        """Test the segment_text function."""
        # Create test chunks
        test_chunks = [
            {"start": 0.0, "end": 5.0, "text": "This is the first sentence about topic A."},
            {"start": 5.0, "end": 10.0, "text": "This is the second sentence about topic A."}, 
            {"start": 10.0, "end": 15.0, "text": "This is the third sentence about a different topic B."},
            {"start": 15.0, "end": 20.0, "text": "This is the fourth sentence about topic B."}
        ]
        
        # Test segmentation
        segments = segment_text(test_chunks)
        
        # Check that we got segments back
        self.assertIsInstance(segments, list)
        self.assertGreaterEqual(len(segments), 1)  # At least one segment should be created
        
        # Check that segments have expected properties
        if segments:
            for segment in segments:
                self.assertIn("start", segment)
                self.assertIn("end", segment) 
                self.assertIn("text", segment)
                self.assertIn("sentence_count", segment)
    
    def test_segment_text_empty(self):
        """Test segment_text with empty input."""
        result = segment_text([])
        self.assertEqual(result, [])
    
    def test_segment_text_single_chunk(self):
        """Test segment_text with a single chunk."""
        single_chunk = [{"start": 0.0, "end": 5.0, "text": "This is a single sentence."}]
        result = segment_text(single_chunk)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["text"], "This is a single sentence.")
    
    def test_load_metadata(self):
        """Test loading metadata."""
        # Create a temporary metadata file
        temp_meta_file = Path(self.test_dir) / "test_metadata.json"
        test_data = {"test.wav": {"status": "done"}}
        
        # Write test metadata
        temp_meta_file.write_text(json.dumps(test_data))
        
        # Temporarily modify the segmentation module to use our test file
        import sys
        sys.path.append('src')
        import segmentation
        original_meta_file = segmentation.META_FILE
        segmentation.META_FILE = temp_meta_file
        
        # Test loading
        loaded_data = load_metadata()
        
        # Restore original path
        segmentation.META_FILE = original_meta_file
        
        self.assertEqual(loaded_data, test_data)


if __name__ == '__main__':
    unittest.main()