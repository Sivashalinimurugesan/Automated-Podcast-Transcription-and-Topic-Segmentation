import unittest
from unittest.mock import patch, MagicMock
from src.keyword_extraction import KeywordExtractor

class TestKeywordExtraction(unittest.TestCase):
    @patch('src.keyword_extraction.KeyBERT')
    def test_extract_keybert(self, MockKeyBERT):
        # Setup mock
        mock_instance = MockKeyBERT.return_value
        mock_instance.extract_keywords.return_value = [('podcast', 0.9), ('ai', 0.8)]
        
        extractor = KeywordExtractor(method='keybert')
        keywords = extractor.extract("This is a podcast about AI.")
        
        self.assertEqual(keywords, ['podcast', 'ai'])

    @patch('src.keyword_extraction.yake.KeywordExtractor')
    @patch('src.keyword_extraction.SentenceTransformer')
    def test_extract_yake_fallback(self, MockST, MockYake):
        # Force YAKE by erroring KeyBERT or choosing method='yake'
        extractor = KeywordExtractor(method='yake')
        
        mock_yake_instance = MockYake.return_value
        mock_yake_instance.extract_keywords.return_value = [('manual', 0.5)]
        
        keywords = extractor.extract("Manual extraction.")
        # Without embedder loaded (mocked), it returns raw yake results
        self.assertEqual(keywords, ['manual'])

    def test_extract_topics(self):
        topics = [{'id': 1, 'text': "Test content"}]
        with patch('src.keyword_extraction.KeyBERT') as MockKB:
            MockKB.return_value.extract_keywords.return_value = [('test', 0.9)]
            
            extractor = KeywordExtractor()
            result = extractor.extract_topics(topics)
            
            self.assertEqual(result[0]['keywords'], ['test'])

if __name__ == '__main__':
    unittest.main()
