import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from sentiment_analysis import SentimentAnalysisAgent
except ImportError:
    # Fallback if running from root
    sys.path.append('src')
    from sentiment_analysis import SentimentAnalysisAgent

def test_emotion():
    print("Initializing Agent...")
    try:
        agent = SentimentAnalysisAgent()
    except Exception as e:
        print(f"Model load failed: {e}")
        return

    texts = [
        "I am so happy that this worked out!",
        "This is absolutely terrible and I hate it.",
        "I am afraid of the dark.",
        "The meeting is at 5 PM."
    ]
    
    print("\nTesting Classification:")
    for t in texts:
        # Test both
        s_label, s_score = agent.analyze_sentiment(t)
        e_label, e_score = agent.analyze_emotion(t)
        print(f"'{t}' -> Sentiment: {s_label} ({s_score:.2f}) | Emotion: {e_label} ({e_score:.2f})")

    print("\nTesting Process Topics:")
    topics = [
        {"id": 1, "text": "I love this!", "start": 0, "end": 10},
        {"id": 2, "text": "This is scary.", "start": 10, "end": 20}
    ]
    processed = agent.process_topics(topics)
    for p in processed:
        print(f"Topic {p['id']}: {p['emotion']} (Score: {p['emotion_score']:.3f}) | Sentiment: {p['sentiment']}")

if __name__ == "__main__":
    test_emotion()
