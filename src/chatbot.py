import logging
import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PodcastChatBot:
    def __init__(self, model_name="google/flan-t5-base"):
        """
        Initializes the Q&A Chatbot with a RAG-compatible generator.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        self.device_name = 'GPU' if self.device == 0 else 'CPU'
        
        logger.info(f"Initializing Chatbot on {self.device_name} with model: {model_name}...")
        
        try:
            # We use text2text-generation for Flan-T5
            self.generator = pipeline(
                "text2text-generation", 
                model=model_name, 
                device=self.device,
                max_length=512
            )
            logger.info("Chatbot model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load chatbot model: {e}")
            self.generator = None
            self.load_error = str(e)

    def generate_answer(self, query, context_topics, intent="SPECIFIC"):
        """
        Generates an answer based on the query and retrieved topics.
        """
        if not self.generator:
            return {"answer": f"I'm sorry, my brain is currently offline. Error: {getattr(self, 'load_error', 'Unknown')}", "references": []}

        if not context_topics:
            return {"answer": "I couldn't find any relevant information in the transcript to answer that.", "references": []}

        # 1. Prepare Context
        # Concatenate summaries or text from top topics
        context_text = ""
        references = []
        
        MAX_CONTEXT_LEN = 2000 # Approximation for 512 token output + prompt
        
        for t in context_topics:
            # Smart Selection:
            # If Summary intent, prefer summary.
            # If Specific intent, prefer raw text to get details.
            if intent == "SUMMARY":
                 text_chunk = t.get('summary') or t.get('text', '')[:500]
            else:
                 # SPECIFIC: Use raw text, but limit length to avoid overflowing
                 text_chunk = t.get('text', '')[:800] # Increased chunk size for detail
            
            # Simple truncation check
            if len(context_text) + len(text_chunk) > MAX_CONTEXT_LEN:
                break
                
            context_text += f"- {text_chunk}\n"
            
            # Save reference for UI
            start_sec = int(t.get('start', 0))
            ts_fmt = f"{start_sec//60}:{start_sec%60:02d}"
            title = t.get('title', 'Segment')
            # Deduplicate references
            ref_str = f"[{ts_fmt}] {title}"
            if ref_str not in references:
                references.append(ref_str)

        # 2. Construct Prompt
        if intent == "SUMMARY":
            prompt = f"""Summarize the following podcast segments into a concise overview of the main topics discussed.
            
Context:
{context_text}

Summary:"""
        else:
            # Flan-T5 prompt format: "question: ... context: ..."
            # Removed strict "say I don't know" to allow best-effort answers
            prompt = f"""Answer the question based on the provided transcript context.
            
Context:
{context_text}

Question: {query}
Answer:"""

        try:
            # 3. Generate
            # Tune generation to prevent repetition loops (common in small models like T5)
            output = self.generator(
                prompt, 
                max_length=512, 
                do_sample=True, 
                temperature=0.7, 
                top_p=0.9,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )[0]['generated_text']
            
            return {
                "answer": output,
                "references": references
            }
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return {
                "answer": f"I encountered an error while thinking: {e}",
                "references": []
            }

    def detect_intent(self, query):
        """
        Detects if the user wants a general summary or specific details.
        """
        summary_keywords = ['summarize', 'summary', 'overview', 'main points', 'what is this about', 'discuss', 'key points']
        query_lower = query.lower()
        
        # specific check for "topic" to avoid "how many topics" triggering summary
        # REMOVED aggressive 'what + topic' check as it causes false positives
        # if "topic" in query_lower and "what" in query_lower:
        #      return "SUMMARY"

        if any(k in query_lower for k in summary_keywords):
            logger.info(f"Intent Detection: 'SUMMARY' triggered by keyword match in '{query}'")
            return "SUMMARY"
            
        logger.info(f"Intent Detection: 'SPECIFIC' (default) for '{query}'")
        return "SPECIFIC"

    def ask(self, query, indexer):
        """
        End-to-end RAG pipeline: Retrieve -> Generate
        With Smart Context Selection.
        """
        if not query or not query.strip():
            return {"answer": "Please ask a question.", "references": []}

        try:
            intent = self.detect_intent(query)
            logger.info(f"Processing Query: '{query}' | Detected Intent: {intent}")
            context_topics = []
            
            if intent == "SUMMARY":
                # Strategy: Retrieve ALL topic summaries for a comprehensive answer
                logger.info("Detected SUMMARY intent. Retrieving full context.")
                # We can access all topics via the indexer's stored topics if exposed, 
                # or we just search with a generic term? 
                # Better: The indexer stores `self.topics`. We need to access that.
                if hasattr(indexer, 'topics') and indexer.topics:
                    context_topics = indexer.topics
                else:
                    # Fallback to search if direct access fails
                    search_results = indexer.search("summary", top_n=10)
                    for res in search_results:
                        t = indexer.get_topic_by_id(res['id'])
                        if t: context_topics.append(t)
            else:
                # Strategy: Specific Search with increased recall (Top 5)
                logger.info("Detected SPECIFIC intent. Searching top 5.")
                search_results = indexer.search(query, top_n=5)
                for res in search_results:
                    full_topic = indexer.get_topic_by_id(res['id'])
                    if full_topic:
                        context_topics.append(full_topic)
            
            # 2. Generate
            response = self.generate_answer(query, context_topics, intent=intent)
            
            return response
            
        except Exception as e:
            logger.error(f"Chatbot failed: {e}")
            return {"answer": "Sorry, something went wrong.", "references": []}
