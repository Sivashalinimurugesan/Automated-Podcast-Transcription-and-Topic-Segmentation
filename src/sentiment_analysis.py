import logging
import torch
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalysisAgent:
    def __init__(self, 
                 sentiment_model="distilbert-base-uncased-finetuned-sst-2-english",
                 emotion_model="j-hartmann/emotion-english-distilroberta-base"):
        """
        Initializes the Sentiment and Emotion Analysis models.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        self.device_name = 'GPU' if self.device == 0 else 'CPU'
        
        logger.info(f"Initializing SentimentAnalysisAgent on {self.device_name}...")

        try:
            # 1. Sentiment Model
            logger.info(f"Loading Sentiment Model: {sentiment_model}")
            self.sentiment_pipe = pipeline(
                "sentiment-analysis", 
                model=sentiment_model, 
                device=self.device
            )

            # 2. Emotion Model
            logger.info(f"Loading Emotion Model: {emotion_model}")
            self.emotion_pipe = pipeline(
                "text-classification", 
                model=emotion_model, 
                return_all_scores=True, 
                device=self.device
            )
            
            logger.info("All models loaded successfully.")
            
        except Exception as e:
            logger.error(f"Failed to load analysis models: {e}")
            self.sentiment_pipe = None
            self.emotion_pipe = None
            raise

    def analyze_sentiment(self, text):
        """
        Analyzes sentiment of text.
        Returns: (label, score) -> ('POSITIVE'|'NEGATIVE', float)
        """
        if not self.sentiment_pipe or not text or not text.strip():
            return "NEUTRAL", 0.0

        try:
            # Use tokenizer truncation instead of naive string slicing
            result = self.sentiment_pipe(text, truncation=True, max_length=512)[0]
            return result['label'], result['score']
        except Exception as e:
            logger.warning(f"Sentiment inference failed: {e}")
            return "NEUTRAL", 0.0

    def analyze_emotion(self, text):
        """
        Analyzes dominant emotion.
        Returns: (label, score)
        Emotions: anger, disgust, fear, joy, neutral, sadness, surprise
        """
        if not self.emotion_pipe or not text or not text.strip():
            return "neutral", 0.0

        try:
            # Use tokenizer truncation
            predictions = self.emotion_pipe(text, truncation=True, max_length=512)
            scores = predictions[0]
            top_emotion = max(scores, key=lambda x: x['score'])
            return top_emotion['label'], top_emotion['score']
        except Exception as e:
            logger.warning(f"Emotion inference failed: {e}")
            return "neutral", 0.0

    def process_topics(self, topics):
        """
        Enriches a list of topic objects with sentiment and emotion data.
        
        Input Topic Structure:
        {
          "id": int,
          "text": str,
          "summary": str,  <-- Preferred for analysis
          "segments": [...]
        }
        
        Output adds:
        {
          "sentiment": str,
          "sentiment_score": float,
          "emotion": str,
          "emotion_score": float
        }
        """
        if not topics:
            return []

        logger.info(f"Starting analysis on {len(topics)} topics...")

        for topic in topics:
            # Prefer summary for cleaner signal, fallback to text
            analysis_text = topic.get('summary') or topic.get('text', '')
            
            # 1. Topic Level Analysis
            s_label, s_score = self.analyze_sentiment(analysis_text)
            e_label, e_score = self.analyze_emotion(analysis_text)
            
            topic['sentiment'] = s_label
            topic['sentiment_score'] = s_score
            topic['emotion'] = e_label
            topic['emotion_score'] = e_score
            
            # 2. Segment Level Analysis (if available)
            # Useful for granular timelines
            if 'segments' in topic:
                for seg in topic['segments']:
                    seg_text = seg.get('text', '')
                    
                    # We can use the same function, maybe lighter? 
                    # For now, consistent reuse ensures accuracy.
                    es_label, es_score = self.analyze_emotion(seg_text)
                    
                    # Optional: Sentiment per segment too? 
                    # Request emphasizes "Emotion Context" for granular flow.
                    # Let's add emotion primarily for the "Emotion Flow" chart.
                    seg['emotion'] = es_label
                    seg['emotion_score'] = es_score
                    
                    if 'speaker' not in seg:
                        seg['speaker'] = "Unknown"

        logger.info("Topic analysis completed.")
        return topics
