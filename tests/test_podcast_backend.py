import unittest
import os
import sys
import shutil
from pathlib import Path


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

try:
    import podcast_backend
except ImportError:
    print("CRITICAL: Could not import 'podcast_backend'. Check your folder structure.")
    sys.exit(1)

class TestPodcastBackend(unittest.TestCase):

    def test_format_time(self):
        """
        Test if seconds are correctly converted to MM:SS format.
        """
        
        self.assertEqual(podcast_backend.format_time(60), "01:00")
       
        self.assertEqual(podcast_backend.format_time(65), "01:05")
        
        self.assertEqual(podcast_backend.format_time(0), "00:00")
        
        self.assertEqual(podcast_backend.format_time(90.5), "01:30")

    def test_extract_keywords_simple(self):
        """
        Test if keyword extraction works on a simple string.
        """
        
        dummy_text = "apple banana apple orange banana apple grape"
        
        
        result = podcast_backend.extract_keywords_text(dummy_text, top_n=2)
        
     
        self.assertIsInstance(result, str)
        
        self.assertIn("apple", result)

    def test_setup_directories(self):
        """
        Test if the directory creation function actually makes folders.
        """
        test_base_dir = "temp_test_data"
        
     
        dirs = podcast_backend.setup_directories(test_base_dir)
        
        
        self.assertTrue(os.path.exists(dirs["audio"]))
        self.assertTrue(os.path.exists(dirs["transcripts"]))
        
        
        if os.path.exists(test_base_dir):
            shutil.rmtree(test_base_dir)

if __name__ == '__main__':
    unittest.main()
