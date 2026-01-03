import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.segmentation import TopicSegmenter

class TestSegmentation(unittest.TestCase):
    @patch('src.segmentation.SentenceTransformer')
    def setUp(self, MockModel):
        self.mock_model = MockModel.return_value
        self.segmenter = TopicSegmenter()

    def test_segment_transcript(self):
        # Setup inputs
        transcript_segments = [
            {'text': "Sentence one.", 'start': 0, 'end': 5},
            {'text': "Sentence two.", 'start': 5, 'end': 10},
            {'text': "Sentence three.", 'start': 10, 'end': 15},
            {'text': "Sentence four.", 'start': 15, 'end': 20},
            {'text': "Sentence five.", 'start': 40, 'end': 45}, # Big gap in time
        ]
        
        # Mock embeddings (random or structured)
        # 5 sentences => 5 embeddings
        self.mock_model.encode.return_value = np.random.rand(5, 384)
        
        # Run segmentation
        # Small window for small test
        topics = self.segmenter.segment_transcript(transcript_segments, window_size=1, min_topic_duration=5.0)
        
        self.assertIsInstance(topics, list)
        if len(topics) > 0:
            self.assertIn('text', topics[0])
            self.assertIn('start', topics[0])
            self.assertIn('end', topics[0])

    def test_empty_transcript(self):
        topics = self.segmenter.segment_transcript([])
        self.assertEqual(topics, [])

if __name__ == '__main__':
    unittest.main()
