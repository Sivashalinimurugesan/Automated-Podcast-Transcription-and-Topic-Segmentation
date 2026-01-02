import unittest
import os
import tempfile
from pathlib import Path
from src.preprocessing import preprocess_audio, load_metadata, save_metadata


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.test_audio_path = os.path.join(self.test_dir, "test_audio.wav")
        
        # Create a simple test audio file (this would be a real audio file in practice)
        # For now, we'll just create a dummy file
        with open(self.test_audio_path, 'w') as f:
            f.write("dummy audio content")
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_preprocess_audio(self):
        """Test the preprocess_audio function."""
        # Test that the function runs without error
        output_path, elapsed_time = preprocess_audio(self.test_audio_path)
        
        # Check that output path is returned
        self.assertIsInstance(output_path, str)
        self.assertGreater(elapsed_time, 0)
    
    def test_load_save_metadata(self):
        """Test loading and saving metadata."""
        # Create test metadata
        test_metadata = {"test_file.wav": {"preprocessing": {"status": "done"}}}
        
        # Save metadata
        temp_meta_file = os.path.join(self.test_dir, "test_metadata.json")
        original_meta_file = "./docs/processing_metadata.json"
        
        # Temporarily change the metadata file location for testing
        import sys
        sys.path.append('src')
        import preprocessing
        preprocessing.META_FILE = temp_meta_file
        
        save_metadata(test_metadata)
        
        # Load the saved metadata
        loaded_metadata = load_metadata()
        
        self.assertEqual(loaded_metadata, test_metadata)


if __name__ == '__main__':
    unittest.main()