import os
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.preprocessing import process_audio

class TestPreprocessing(unittest.TestCase):
    @patch('src.preprocessing.librosa.load')
    @patch('src.preprocessing.nr.reduce_noise')
    @patch('src.preprocessing.sf.write')
    def test_process_audio(self, mock_write, mock_reduce_noise, mock_load):
        # Setup mocks
        mock_load.return_value = (np.array([0.1, 0.2, 0.3]), 16000)
        mock_reduce_noise.return_value = np.array([0.05, 0.15, 0.25])
        
        # Temporary directories
        input_file = "test_audio.mp3"
        output_dir = "test_processed"
        
        # Execute
        result_path = process_audio(input_file, output_dir)
        
        # Verify
        mock_load.assert_called_once()
        mock_reduce_noise.assert_called_once()
        mock_write.assert_called_once()
        
        expected_output = os.path.join(output_dir, "test_audio_processed.wav")
        self.assertEqual(result_path, expected_output)

        # Check normalization logic (indirectly via what's passed to write)
        # We can inspect the args passed to sf.write if we want strict checking
        args, _ = mock_write.call_args
        # args[0] is path, args[1] is data, args[2] is sr
        self.assertEqual(args[0], expected_output)
        self.assertEqual(args[2], 16000)

if __name__ == '__main__':
    unittest.main()
