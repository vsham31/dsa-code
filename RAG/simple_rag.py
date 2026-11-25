from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from dotenv import load_dotenv

from paragraph_chunks import create_paragraph_chunks

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
groq_model_name = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")
# Optional fallback, e.g. GROQ_FALLBACK_MODEL_NAME=openai/gpt-oss-20b
groq_fallback_model_name = os.getenv("GROQ_FALLBACK_MODEL_NAME", "openai/gpt-oss-20b")
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

# normal overlap chunking
def create_chunks(text, chunk_size=120, overlap=20):
    chunks=[]
    start=0

    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        start=end-overlap
    return chunks

# chunks=create_chunks(
#     text=text,
#     chunk_size=120,
#     overlap=20,
# )


chunks=create_paragraph_chunks(text=text, max_chars=300)

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

import time
from groq import Groq, APIStatusError, APIConnectionError

if not groq_key:
    raise SystemExit("GROQ_API_KEY is not set. Add it to RAG/.env (get one at console.groq.com).")

groq_client = Groq(api_key=groq_key)

RETRYABLE = (429, 500, 502, 503, 504)


def generate_with_retry(prompt, models, max_retries=2):
    """Call Groq, retrying transient errors with exponential backoff,
    then fall through to the next model in `models`."""
    last_error = None
    for model in models:
        delay = 2
        for attempt in range(1, max_retries + 1):
            try:
                print("model: ", model)
                resp = groq_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                return resp.choices[0].message.content
            except APIStatusError as e:
                last_error = e
                if e.status_code not in RETRYABLE:
                    raise
                print(f"[{model}] {e.status_code} on attempt {attempt}/{max_retries}; retrying in {delay}s...")
            except APIConnectionError as e:
                last_error = e
                print(f"[{model}] connection error on attempt {attempt}/{max_retries}; retrying in {delay}s...")
            if attempt < max_retries:
                time.sleep(delay)
                delay = min(delay * 2, 30)
        print(f"[{model}] still unavailable, trying next model (if any).")
    raise last_error


models_to_try = [m for m in (groq_model_name, groq_fallback_model_name) if m]

print("retry models: ", models_to_try)
answer = generate_with_retry(prompt, models_to_try)

print("\nLLM Answer: ")
print(answer)


# new implementation of rag

# with the top k retreival from documents instead of array