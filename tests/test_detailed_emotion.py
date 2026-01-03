import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sentiment_analysis import SentimentAnalysisAgent

class MockPipe:
    def __call__(self, text, **kwargs):
        # Mock response based on text content
        if "happy" in text:
            return [[{'label': 'joy', 'score': 0.9}]]
        elif "sad" in text:
            return [[{'label': 'sadness', 'score': 0.8}]]
        else:
            return [[{'label': 'neutral', 'score': 0.5}]]

class TestDetailedEmotion(unittest.TestCase):
    def setUp(self):
        # Patch the pipeline loading
        self.agent = SentimentAnalysisAgent()
        # Mock the internal pipeline
        self.agent.emotion_pipe = MockPipe()
        # Mock sentiment pipe as well to avoid errors
        self.agent.sentiment_pipe = lambda x: [{'label': 'neutral', 'score': 0.5}]

    def test_segment_emotion_processing(self):
        topics = [{
            "id": 1,
            "text": "Overall topic text is happy.",
            "segments": [
                {"text": "I am so happy!", "speaker": "SPEAKER_01"},
                {"text": "I am very sad.", "speaker": "SPEAKER_02"}
            ]
        }]
        
        result = self.agent.process_topics(topics)
        
        # Check Topic Level
        self.assertEqual(result[0]['emotion'], 'joy')
        
        # Check Segment Level
        segments = result[0]['segments']
        self.assertEqual(len(segments), 2)
        
        # Segment 1
        self.assertEqual(segments[0]['emotion'], 'joy')
        self.assertEqual(segments[0]['speaker'], 'SPEAKER_01')
        
        # Segment 2
        self.assertEqual(segments[1]['emotion'], 'sadness')
        self.assertEqual(segments[1]['speaker'], 'SPEAKER_02')
        
        print("\n✅ Detailed emotion analysis verified.")

if __name__ == '__main__':
    unittest.main()
