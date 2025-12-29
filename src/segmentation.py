import nltk
nltk.download("punkt")
nltk.download("punkt_tab")  # needed in latest NLTK for sentence tokenization
from nltk.tokenize import TextTilingTokenizer, sent_tokenize
from keybert import KeyBERT
import nltk
nltk.download('stopwords')

tt = TextTilingTokenizer()

def segment_document(doc_text):
    """
    Segment a document into topic blocks using TextTiling.
    If TextTiling fails (too short), return the whole doc as one segment.
    """
    try:
        segments = tt.tokenize(doc_text)
    except Exception:
        segments = [doc_text]
    return [seg.strip() for seg in segments if seg.strip()]


docs_df["segments"] = docs_df["document"].apply(segment_document)

# Show segments for first document
print("First document segments:")
for i, seg in enumerate(docs_df["segments"].iloc[0]):
    print(f"\n--- Segment {i+1} ---")
    print(seg[:300])


