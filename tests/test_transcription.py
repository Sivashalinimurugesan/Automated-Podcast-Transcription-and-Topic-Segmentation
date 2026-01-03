import unittest
from unittest.mock import patch, MagicMock
import os
import json
from src.transcription import Transcriber

class TestTranscription(unittest.TestCase):
    @patch('src.transcription.WhisperModel')
    def setUp(self, MockModel):
        self.mock_model_instance = MockModel.return_value
        self.transcriber = Transcriber(model_size="tiny", device="cpu")

    def test_transcribe(self):
        # Mock segments generator
        Segment = MagicMock()
        Segment.start = 0.0
        Segment.end = 1.0
        Segment.text = "Hello world"
        
        # transcribe returns (segments_generator, info)
        self.mock_model_instance.transcribe.return_value = ([Segment], MagicMock(language="en", language_probability=0.99))
        
        with patch('os.path.exists', return_value=True):
            result = self.transcriber.transcribe("dummy.wav")
            
        self.assertEqual(result['text'], "Hello world")
        self.assertEqual(len(result['segments']), 1)
        self.assertEqual(result['language'], "en")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.makedirs')
    def test_save_outputs(self, mock_makedirs, mock_file):
        result = {
            "text": "Hello world",
            "segments": [{"start": 0, "end": 1, "text": "Hello world"}],
            "language": "en"
        }
        
        audio_filename = "test_audio.wav"
        txt_path, json_path = self.transcriber.save_outputs(result, audio_filename, "test_transcripts", "test_segments")
        
        self.assertTrue(txt_path.endswith('.txt'))
        self.assertTrue(json_path.endswith('.json'))
        
        # Verify file writes
        # We expect 2 open calls (one for txt, one for json)
        self.assertEqual(mock_file.call_count, 2)
        mock_makedirs.assert_called()

if __name__ == '__main__':
    unittest.main()
