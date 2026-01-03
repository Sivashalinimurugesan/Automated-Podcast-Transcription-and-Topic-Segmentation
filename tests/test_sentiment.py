import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sentiment_analysis import SentimentAnalysisAgent

class TestSentimentAnalysis(unittest.TestCase):
    def setUp(self):
        # Patch pipelines to avoid loading real models
        with patch('sentiment_analysis.pipeline') as mock_pipeline:
            self.agent = SentimentAnalysisAgent()
            # Restore the mocks for individual tests to configure
            self.agent.sentiment_pipe = MagicMock()
            self.agent.emotion_pipe = MagicMock()

    def test_sentiment_output(self):
        # Mock sentiment return
        self.agent.sentiment_pipe.return_value = [{'label': 'POSITIVE', 'score': 0.99}]
        
        label, score = self.agent.analyze_sentiment("This is great!")
        self.assertEqual(label, 'POSITIVE')
        self.assertEqual(score, 0.99)

    def test_emotion_output(self):
        # Mock emotion return
        self.agent.emotion_pipe.return_value = [[
            {'label': 'joy', 'score': 0.8},
            {'label': 'anger', 'score': 0.1},
            {'label': 'neutral', 'score': 0.1}
        ]]
        
        label, score = self.agent.analyze_emotion("I am so happy!")
        self.assertEqual(label, 'joy')
        self.assertEqual(score, 0.8)

    def test_process_topics_enrichment(self):
        topics = [
            {"id": 1, "text": "I hate this.", "summary": "Negative vibration."}
        ]
        
        # Configure mocks
        self.agent.sentiment_pipe.return_value = [{'label': 'NEGATIVE', 'score': 0.95}]
        self.agent.emotion_pipe.return_value = [[{'label': 'anger', 'score': 0.9}]]
        
        result = self.agent.process_topics(topics)
        
        self.assertEqual(result[0]['sentiment'], 'NEGATIVE')
        self.assertEqual(result[0]['sentiment_score'], 0.95)
        self.assertEqual(result[0]['emotion'], 'anger')
        self.assertEqual(result[0]['emotion_score'], 0.9)
        
    def test_empty_input_safety(self):
        # Should handle without crashing
        self.agent.sentiment_pipe.side_effect = Exception("Should not be called")
        
        label, score = self.agent.analyze_sentiment("")
        self.assertEqual(label, "NEUTRAL")

if __name__ == '__main__':
    unittest.main()
