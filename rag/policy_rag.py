"""Build and query a persistent, local policy index."""
from pathlib import Path
import re
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def lookup_policy(question: str) -> str:
    """Retrieve top matching policy chunks using SentenceTransformers cosine similarity."""
    from sentence_transformers import SentenceTransformer
    
    # 1. Load the model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    # 2. Load and split documents
    chunks = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Split by paragraph or lines
            for paragraph in content.split("\n\n"):
                paragraph = paragraph.strip()
                if paragraph:
                    chunks.append(paragraph)
        except Exception as e:
            print(f"Error loading {path}: {e}")
                
    if not chunks:
        return "I'm sorry, I couldn't find that information in our flower shop policies."
        
    # 3. Compute embeddings
    chunk_embeddings = model.encode(chunks, convert_to_numpy=True)
    question_embedding = model.encode(question, convert_to_numpy=True)
    
    # 4. Compute cosine similarity
    dots = np.dot(chunk_embeddings, question_embedding)
    norms = np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(question_embedding)
    # Avoid divide by zero
    norms[norms == 0] = 1e-9
    similarities = dots / norms
    
    # 5. Get top matches (top 3 matching chunks with similarity > 0.25)
    top_indices = np.argsort(similarities)[::-1]
    best_chunks = []
    for idx in top_indices:
        if similarities[idx] > 0.25:
            best_chunks.append(chunks[idx])
        if len(best_chunks) >= 3:
            break
            
    if not best_chunks:
        return "I'm sorry, I couldn't find that information in our flower shop policies."
        
    context = "\n\n".join(best_chunks)
    
    # Validation word overlap logic to ensure relevance
    query_terms = {word for word in re.findall(r"[a-z0-9]+", question.lower()) if len(word) > 3}
    context_terms = set(re.findall(r"[a-z0-9]+", context.lower()))
    if not query_terms.intersection(context_terms):
        return "I'm sorry, I couldn't find that information in our flower shop policies."
        
    return f"Policy information found:\n{context}"
