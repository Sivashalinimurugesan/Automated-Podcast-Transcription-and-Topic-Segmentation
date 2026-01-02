import unittest
import tempfile
import os
import json
from pathlib import Path
from src.transcription import get_audio_duration, transcribe_audio, load_metadata


class TestTranscription(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.test_audio_path = os.path.join(self.test_dir, "test_audio.wav")
        
        # Create a simple test audio file
        with open(self.test_audio_path, 'w') as f:
            f.write("dummy audio content")
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_get_audio_duration(self):
        """Test the get_audio_duration function."""
        # This will fail with our dummy file, but we can at least test that it raises expected errors
        with self.assertRaises(Exception):
            # This should fail since our file is not a real audio file
            duration = get_audio_duration(Path(self.test_audio_path))
    
    def test_load_metadata(self):
        """Test loading metadata."""
        # Create a temporary metadata file
        temp_meta_file = Path(self.test_dir) / "test_metadata.json"
        test_data = {"test.wav": {"status": "done"}}
        
        # Write test metadata
        temp_meta_file.write_text(json.dumps(test_data))
        
        # Temporarily modify the transcription module to use our test file
        import sys
        sys.path.append('src')
        import transcription
        original_meta_file = transcription.META_FILE
        transcription.META_FILE = temp_meta_file
        
        # Test loading
        loaded_data = load_metadata()
        
        # Restore original path
        transcription.META_FILE = original_meta_file
        
        self.assertEqual(loaded_data, test_data)


if __name__ == '__main__':
    unittest.main()