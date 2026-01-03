import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from chatbot import PodcastChatBot

class TestPodcastChatBot(unittest.TestCase):
    def setUp(self):
        # Mock the pipeline so we don't download models during test
        with patch('chatbot.pipeline') as mock_pipeline:
            self.bot = PodcastChatBot()
            self.bot.generator = MagicMock() # Mock the generator instance
            self.bot.generator.side_effect = lambda x: [{'generated_text': 'This is a mock answer.'}]
        
        self.indexer = MagicMock()

    def test_ask_empty_query(self):
        result = self.bot.ask("", MagicMock())
        self.assertEqual(result['answer'], "Please ask a question.")

    def test_ask_no_context(self):
        # Mock indexer to return empty results
        mock_indexer = MagicMock()
        mock_indexer.search.return_value = []
        
        result = self.bot.ask("Hello?", mock_indexer)
        self.assertIn("couldn't find any relevant information", result['answer'])

    def test_detect_intent(self):
        # Test Summary keywords
        self.assertEqual(self.bot.detect_intent("Summarize this podcast"), "SUMMARY")
        self.assertEqual(self.bot.detect_intent("What is the main topic?"), "SUMMARY")
        self.assertEqual(self.bot.detect_intent("Give me an overview"), "SUMMARY")
        
        # Test Specific queries
        self.assertEqual(self.bot.detect_intent("What did they say about allergies?"), "SPECIFIC")
        self.assertEqual(self.bot.detect_intent("Who is the guest?"), "SPECIFIC")

    def test_ask_summary_intent(self):
        # Mock indexer to have topics directly
        self.indexer.topics = [{'id': 1, 'text': 'Topic 1'}, {'id': 2, 'text': 'Topic 2'}]
        
        # Query that triggers summary
        response = self.bot.ask("Summarize the podcast", self.indexer)
        
        # Should not call search, but use direct topics
        self.indexer.search.assert_not_called()
        self.assertIn("answer", response)

    def test_ask_specific_intent(self):
        # Setup mock search return
        self.indexer.search.return_value = [{'id': 0, 'score': 0.9}]
        self.indexer.get_topic_by_id.return_value = {'text': "Specific info", 'start': 0, 'title': 'Test'}
        
        self.bot.ask("Specific question", self.indexer)
        
        # Should call search with top_n=5
        self.indexer.search.assert_called_with("Specific question", top_n=5)

    def test_ask_with_context(self):
        # Mock indexer to return valid topics
        mock_indexer = MagicMock()
        mock_indexer.search.return_value = [{'id': 1, 'score': 0.9}]
        mock_indexer.get_topic_by_id.return_value = {
            'id': 1, 'start': 0, 'text': 'We discussed AI.', 'summary': 'AI discussion', 'title': 'Intro'
        }
        
        result = self.bot.ask("What about AI?", mock_indexer)
        
        # Check if generation was called
        self.bot.generator.assert_called_once()
        self.assertEqual(result['answer'], 'This is a mock answer.')
        self.assertIn('[0:00] Intro', result['references'])

if __name__ == '__main__':
    unittest.main()
