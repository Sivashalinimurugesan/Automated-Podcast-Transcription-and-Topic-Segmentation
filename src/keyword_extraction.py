import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string
import warnings

warnings.filterwarnings("ignore")

# --- NLTK SETUP (Auto-Download) ---
def download_nltk_resources():
    """Ensures necessary NLTK data is available."""
    resources = ['punkt', 'stopwords', 'punkt_tab']
    for res in resources:
        try:
            nltk.data.find(f'tokenizers/{res}')
        except LookupError:
            try:
                nltk.download(res, quiet=True)
            except Exception:
                pass # Handle offline cases gracefully

download_nltk_resources()

def extract_keywords(text, top_n=5):
    """
    Extracts top keywords for a single segment using NLTK.
    """
    if not text: return []
    
    try:
        # 1. Tokenize & Lowercase
        tokens = word_tokenize(text.lower())
        
        # 2. Get Stopwords & Punctuation
        stop_words = set(stopwords.words('english'))
        punctuation = set(string.punctuation)
        
        # 3. Filter Tokens
        filtered_tokens = [
            word for word in tokens 
            if word not in stop_words 
            and word not in punctuation 
            and len(word) > 3 # Ignore short words like "is", "go"
            and word.isalnum() # Ensure it's alphanumeric
        ]
        
        # 4. Count Frequency
        common_words = Counter(filtered_tokens).most_common(top_n)
        return [word for word, count in common_words]
        
    except Exception as e:
        print(f"NLTK Error: {e}")
        return []

def get_global_keyword_counts(full_text, top_n=20):
    """
    Analyzes the WHOLE transcript to count word frequencies for the Bubble Chart.
    Returns: [{'keyword': 'Money', 'count': 15}, ...]
    """
    if not full_text: return []

    try:
        # 1. Tokenize & Lowercase
        tokens = word_tokenize(full_text.lower())
        
        # 2. Get Stopwords
        stop_words = set(stopwords.words('english'))
        punctuation = set(string.punctuation)
        
        # 3. Filter
        filtered_tokens = [
            word for word in tokens 
            if word not in stop_words 
            and word not in punctuation 
            and len(word) > 4 # Stricter length for global bubbles
            and word.isalnum()
        ]
        
        # 4. Count & Format for UI
        counter = Counter(filtered_tokens)
        most_common = counter.most_common(top_n)
        
        # Convert to list of dicts for Plotly
        result = [{"keyword": word.title(), "count": count} for word, count in most_common]
        return result

    except Exception as e:
        print(f"Global Count Error: {e}")
        return []