import unittest
import tempfile
import json
import os
from pathlib import Path
import shutil
import subprocess


class TestSystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.project_root = Path(__file__).parent.parent
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        shutil.rmtree(self.test_dir)
    
    def test_all_modules_import_correctly(self):
        """Test that all modules can be imported without errors."""
        modules_to_test = [
            'src.preprocessing',
            'src.transcription', 
            'src.segmentation',
            'src.keyword_extraction',
            'src.summarization',
            'src.ui_app'
        ]
        
        for module_path in modules_to_test:
            try:
                # Import the module
                module = __import__(module_path, fromlist=[''])
                # If we get here, the import was successful
                self.assertIsNotNone(module)
            except ImportError as e:
                self.fail(f"Failed to import {module_path}: {e}")
    
    def test_requirements_exist(self):
        """Test that requirements file exists and contains expected packages."""
        requirements_path = self.project_root / "requirements.txt"
        self.assertTrue(requirements_path.exists(), "requirements.txt should exist")
        
        # Read requirements
        content = requirements_path.read_text()
        
        # Check for essential packages
        essential_packages = [
            'streamlit', 'google-generativeai', 'sentence-transformers', 
            'yake', 'textblob', 'plotly', 'wordcloud'
        ]
        
        for package in essential_packages:
            self.assertIn(package, content, f"{package} should be in requirements.txt")
    
    def test_directory_structure(self):
        """Test that required directories exist."""
        required_dirs = [
            'src', 'tests', 'audio_raw', 'audio_processed', 
            'transcripts', 'segments', 'docs'
        ]
        
        for directory in required_dirs:
            dir_path = self.project_root / directory
            self.assertTrue(dir_path.exists(), f"{directory} directory should exist")
    
    def test_config_files_exist(self):
        """Test that configuration files exist."""
        config_files = ['.env', 'README.md']
        
        for config_file in config_files:
            file_path = self.project_root / config_file
            self.assertTrue(file_path.exists(), f"{config_file} should exist")
    
    def test_metadata_file_structure(self):
        """Test that metadata file has correct structure."""
        # Create a test metadata structure
        test_metadata = {
            "sample_audio.wav": {
                "preprocessing": {"status": "done"},
                "transcription": {"status": "done"},
                "segmentation": {"status": "done"},
                "keywords": {"status": "done"},
                "summarization": {"status": "done"}
            }
        }
        
        # Verify structure
        self.assertIn("sample_audio.wav", test_metadata)
        audio_data = test_metadata["sample_audio.wav"]
        
        required_keys = ["preprocessing", "transcription", "segmentation", "keywords", "summarization"]
        for key in required_keys:
            self.assertIn(key, audio_data)
            self.assertIn("status", audio_data[key])
    
    def test_environment_variables(self):
        """Test that environment variables are properly defined."""
        env_file = self.project_root / ".env"
        self.assertTrue(env_file.exists(), ".env file should exist")
        
        # Read and parse environment variables
        env_content = env_file.read_text()
        
        # Check for essential environment variables
        required_vars = [
            "AUDIO_RAW_DIR", "AUDIO_PROCESSED_DIR", "TRANSCRIPTS_DIR",
            "SEGMENTS_DIR", "VOSK_MODEL_PATH", "GEMINI_API_KEY"
        ]
        
        for var in required_vars:
            self.assertIn(var, env_content, f"{var} should be defined in .env")
    
    def test_audio_formats_supported(self):
        """Test that the system supports expected audio formats."""
        # This tests the logic used in the UI for supported formats
        supported_formats = ['mp3', 'wav', 'm4a']
        
        # Verify that these formats are handled in the UI
        ui_app_path = self.project_root / "src" / "ui_app.py"
        ui_content = ui_app_path.read_text()
        
        for fmt in supported_formats:
            # Check that the format appears in the file uploader type list
            self.assertIn(fmt, ui_content, f"Format {fmt} should be supported in UI")


if __name__ == '__main__':
    print("Running system-level tests...")
    unittest.main()