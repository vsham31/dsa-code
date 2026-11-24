from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_model_name = os.getenv('GEMINI_MODEL_NAME')
gemini_key=os.getenv("GEMINI_API_KEY")
embedding_model_name=os.getenv("EMBEDDING_MODEL")

# loading embedding model

embeddingModel = SentenceTransformer(embedding_model_name)

# knowledge base
# Resolve this file relative to the script, rather than the shell's current
# working directory, so `python3 RAG/simple_rag.py` works from the repo root.
knowledge_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge.txt")

# with open("/home/extinct/Downloads/dsa-code/RAG/knowledge.txt", "r", encoding="utf-8") as file:
#     text = file.read()


with open(knowledge_path, "r", encoding="utf-8") as file:
    text = file.read()

print("Original text: ")
print(text)

# chunking

def create_chunks(text, chunk_size=120, overlap=20):
    chunks=[]
    start=0

    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        start=end-overlap
    return chunks

chunks=create_chunks(
    text=text,
    chunk_size=120,
    overlap=20,
)

print("\nChunks:")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}: ")
    print(chunk)



# documents = [
#     "Python is a dynamically typed programming language.",
#     "PostgreSQL is a relational database management system.",
#     "Docker packages applications and their dependencies into containers.",
#     "Kubernetes is used to orchestrate and manage containers.",
#     "Redis is an in-memory data store commonly used for caching."
# ]

# convert documents into embeddings

documentEmbeddings = embeddingModel.encode(chunks)

# question of user

# query = "Which technology is used to manage containers?"

query = input("Ask a question: ")

# make embeddings of query

queryEmbeddings = embeddingModel.encode([query])

# compare query & document vectors 

scores = cosine_similarity(
    queryEmbeddings,
    documentEmbeddings
)[0]

# print the scores

for document, score in zip(chunks, scores):
    print(f"{score: .4f} -> {document}")

# find most similar documents

bestMatchIndex=scores.argmax()

print("\n Best match : ")
print(chunks[bestMatchIndex])
print('documentEmbeddings.shape', documentEmbeddings.shape)
query_embedding = embeddingModel.encode([query])
print('query_embedding.shape', query_embedding.shape)

top_k=3 # top k documents

top_indices = np.argsort(scores)[::-1][:top_k]

print("\n Top results:")

retreived_documents = []

for index in top_indices:
    retreived_documents.append(chunks[index])
    print(f"{scores[index]:.4f}->{chunks[index]}")

# -------------------------
# 5. Build RAG context
# -------------------------

context = "\n".join(retreived_documents)

prompt = f"""
You are a helpful assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
say "I don't know based on the provided context."

Context:
{context}

Question:
{query}

Answer:
"""

# -------------------------
# 6. Call LLM
# -------------------------

client = genai.Client(api_key=gemini_key)

import time
from google.genai import errors as genai_errors

# Optional fallback model, e.g. GEMINI_FALLBACK_MODEL_NAME=gemini-2.0-flash
fallback_model_name = os.getenv("GEMINI_FALLBACK_MODEL_NAME")


def generate_with_retry(prompt, models, max_retries=5):
    """Retry on transient 429/500/503/504 errors with exponential backoff,
    then fall through to the next model in `models`."""
    last_error = None
    for model in models:
        delay = 2
        for attempt in range(1, max_retries + 1):
            try:
                return client.models.generate_content(model=model, contents=prompt)
            except genai_errors.APIError as e:
                last_error = e
                if e.code not in (429, 500, 503, 504):
                    raise
                print(f"[{model}] {e.code} on attempt {attempt}/{max_retries}; retrying in {delay}s...")
                time.sleep(delay)
                delay = min(delay * 2, 30)
        print(f"[{model}] still unavailable, trying next model (if any).")
    raise last_error


models_to_try = [m for m in (gemini_model_name, fallback_model_name) if m]
response = generate_with_retry(prompt, models_to_try)

print("\nLLM Answer: ")
print(response.text)


# new implementation of rag

# with the top k retreival from documents instead of array