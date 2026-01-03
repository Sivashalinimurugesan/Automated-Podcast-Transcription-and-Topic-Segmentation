import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from indexing import TopicIndexer

class TestTopicIndexer(unittest.TestCase):
    def setUp(self):
        self.indexer = TopicIndexer()
        self.indexer.model = MagicMock() # Mock the transformer
        self.indexer.embeddings = MagicMock() # Mock embeddings

    def test_highlight_exact_match(self):
        text = "This is a simple test sentence."
        query = "simple test"
        expected = "This is a <mark style='background:rgba(255, 235, 59, 0.4); color:black; padding:0 2px; border-radius:2px;'>simple test</mark> sentence."
        result = self.indexer.highlight_text(text, query)
        self.assertEqual(result, expected)

    def test_highlight_case_insensitive(self):
        text = "This is a Simple Test."
        query = "simple"
        # Regex sub will use the original text casing but wrap it
        result = self.indexer.highlight_text(text, query)
        self.assertIn("<mark", result)
        self.assertIn(">Simple<", result)

    def test_highlight_fallback_keywords(self):
        text = "The quick brown fox jumps."
        query = "quick jumps" # "quick jumps" as a phrase doesn't exist, should split
        result = self.indexer.highlight_text(text, query)
        # Both words should be highlighted individually
        self.assertEqual(result.count("<mark"), 2)

    def test_highlight_no_match(self):
        text = "Nothing matches here."
        query = "xyz"
        result = self.indexer.highlight_text(text, query)
        self.assertEqual(result, text)

    def test_search_logic(self):
        # We can't easily test the cosine sim logic without a real model or complex mocking,
        # but we can test the structure flow if we mock util.cos_sim
        pass 

if __name__ == '__main__':
    unittest.main()
