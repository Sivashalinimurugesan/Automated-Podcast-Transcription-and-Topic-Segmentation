import unittest
import io
from server import app  # Importing your Flask app

class TestPodcastBackend(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """Test 1: Check if the backend is running (Health Check)."""
        response = self.app.get('/')
        # We expect a 404 because you don't have a root '/' route, 
        # or a 200 if you added one. Let's just check it doesn't crash (500).
        self.assertNotEqual(response.status_code, 500)
        print("\n[PASS] Server is running and reachable.")

    def test_no_file_upload(self):
        """Test 2: Check what happens if we upload NOTHING."""
        response = self.app.post('/api/upload', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file part', response.data)
        print("[PASS] Server correctly rejected empty request.")

    def test_invalid_file_extension(self):
        """Test 3: Check if it rejects non-audio files (like a .txt file)."""
        data = {
            'file': (io.BytesIO(b"fake text content"), 'test.txt')
        }
        response = self.app.post('/api/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid file type', response.data)
        print("[PASS] Server correctly rejected .txt file.")

if __name__ == '__main__':
    print("Starting Automated Tests...")
    unittest.main()