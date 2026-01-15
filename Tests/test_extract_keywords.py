import unittest
from extract_keywords import extract_keywords

class TestExtractKeywords(unittest.TestCase):

    def test_empty_text(self):
        self.assertEqual(extract_keywords(""), [])
        self.assertEqual(extract_keywords("   "), [])

    def test_short_text(self):
        self.assertEqual(extract_keywords("too short"), [])

    def test_basic_extraction(self):
        text = (
            "Machine learning enables computers to learn from data. "
            "Machine learning models improve with more data."
        )
        keywords = extract_keywords(text, top_n=5)
        self.assertTrue(len(keywords) <= 5)
        self.assertTrue(all(isinstance(k, str) for k in keywords))

    def test_lowercase_keywords(self):
        keywords = extract_keywords(
            "Artificial Intelligence and Artificial Intelligence systems"
        )
        for kw in keywords:
            self.assertEqual(kw, kw.lower())

    def test_no_substring_duplicates(self):
        text = (
            "Neural networks are a type of neural network architecture "
            "used in deep neural networks."
        )
        keywords = extract_keywords(text)

        for i, k1 in enumerate(keywords):
            for k2 in keywords[i + 1:]:
                self.assertNotIn(k1, k2)
                self.assertNotIn(k2, k1)

if __name__ == "__main__":
    unittest.main()
