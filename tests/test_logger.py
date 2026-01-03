import os
import shutil
import unittest
import src.logger  # Need this to patch the global
from src.logger import SessionLogger

class TestSessionLogger(unittest.TestCase):
    def setUp(self):
        # Clean up logs directory before test if needed
        # On Windows, we might fail to delete if a file is open.
        self.test_logs_dir = os.path.join(src.logger.LOGS_DIR, "test_logs")
        if os.path.exists(self.test_logs_dir):
            shutil.rmtree(self.test_logs_dir, ignore_errors=True)
        os.makedirs(self.test_logs_dir, exist_ok=True)
        
        # Patch LOGS_DIR
        self.original_logs_dir = src.logger.LOGS_DIR
        src.logger.LOGS_DIR = self.test_logs_dir

    def tearDown(self):
        # Restore
        src.logger.LOGS_DIR = self.original_logs_dir
        
        # Clean up after tests - ignoring errors if files are locked
        if os.path.exists(self.test_logs_dir):
            shutil.rmtree(self.test_logs_dir, ignore_errors=True)

    def test_start_new_session(self):
        session_id, log_path = SessionLogger.start_new_session()
        self.assertIsNotNone(session_id)
        self.assertTrue(os.path.exists(log_path))
        self.assertTrue(log_path.endswith('.log'))
        self.assertEqual(SessionLogger.output_log_file_path(), log_path)

    def test_singleton_behavior(self):
        id1, path1 = SessionLogger.start_new_session()
        id2, path2 = SessionLogger.start_new_session()
        
        # Should be able to start multiple sessions, but current points to latest
        self.assertNotEqual(id1, id2)
        self.assertNotEqual(path1, path2)
        self.assertEqual(SessionLogger.output_log_file_path(), path2)

if __name__ == '__main__':
    unittest.main()
