import unittest
import sys
import os
from pathlib import Path
import tempfile


class TestUIApp(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_ui_app_import(self):
        """Test that UI app can be imported without errors."""
        try:
            # Add src to path to import the UI app
            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            import ui_app
            # If we get here, the import was successful
            self.assertTrue(True)
        except ImportError as e:
            # If there's an import error, the test fails
            self.fail(f"Failed to import ui_app: {e}")
    
    def test_ui_app_functions_exist(self):
        """Test that expected functions exist in ui_app."""
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        import ui_app
        
        # Check that required functions exist
        self.assertTrue(hasattr(ui_app, 'load_metadata'))
        self.assertTrue(hasattr(ui_app, 'save_metadata'))
        self.assertTrue(hasattr(ui_app, 'load_json'))
        self.assertTrue(hasattr(ui_app, 'compute_sentiment'))
    
    def test_metadata_operations(self):
        """Test basic metadata operations."""
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        import ui_app
        
        # Create a temporary metadata file for testing
        temp_meta_file = Path(self.test_dir) / "test_processing_metadata.json"
        
        # Temporarily modify the ui_app to use our test file
        original_meta_file = ui_app.META_FILE
        ui_app.META_FILE = temp_meta_file
        
        try:
            # Test save and load operations
            test_data = {"test.wav": {"status": "done"}}
            ui_app.save_metadata(test_data)
            
            loaded_data = ui_app.load_metadata()
            self.assertEqual(loaded_data, test_data)
        finally:
            # Restore original path
            ui_app.META_FILE = original_meta_file
    
    def test_json_loader(self):
        """Test the load_json function."""
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        import ui_app
        
        # Create a temporary JSON file
        temp_json_file = Path(self.test_dir) / "test.json"
        test_data = [{"text": "test", "start": 0.0, "end": 10.0}]
        
        temp_json_file.write_text(str(test_data).replace("'", '"'))
        
        # Test loading JSON
        loaded_data = ui_app.load_json(temp_json_file)
        self.assertIsInstance(loaded_data, list)
        
        # Test loading non-existent file
        non_existent = Path(self.test_dir) / "non_existent.json"
        empty_data = ui_app.load_json(non_existent)
        self.assertEqual(empty_data, [])


if __name__ == '__main__':
    unittest.main()