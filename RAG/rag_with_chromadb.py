from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from dotenv import load_dotenv
import chromadb
from paragraph_chunks import create_paragraph_chunks

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
groq_model_name = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")
# Optional fallback, e.g. GROQ_FALLBACK_MODEL_NAME=openai/gpt-oss-20b
groq_fallback_model_name = os.getenv("GROQ_FALLBACK_MODEL_NAME", "openai/gpt-oss-20b")
embedding_model_name=os.getenv("EMBEDDING_MODEL")

chroma_client = chromadb.Client()

db = chroma_client.create_collection(name="rag_knowledge")

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


chunks=create_paragraph_chunks(text=text, max_chars=100)

for i, chunk in enumerate(chunks):
    embedding = embeddingModel.encode(chunk).tolist()

    db.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embedding]
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

# queryEmbeddings = embeddingModel.encode([query])

queryEmbedding = embeddingModel.encode(query).tolist()

# compare query & document vectors 

top_k=3 # top k documents

results=db.query(
    query_embeddings=[queryEmbedding],
    n_results=top_k
)

# scores = cosine_similarity(
#     queryEmbeddings,
#     documentEmbeddings
# )[0]

# print the scores

retreived_documents=results["documents"][0]
retreived_ids=results["ids"][0]
retreived_distances=results["distances"][0]

# Chroma returns results sorted best-first (lowest distance = most similar)

print("\n Best match : ")
print(f"id={retreived_ids[0]} distance={retreived_distances[0]:.4f}")
print(retreived_documents[0])

print(f"\n Top {top_k} results:")

for rank, (chunk_id, distance, chunk) in enumerate(
    zip(retreived_ids, retreived_distances, retreived_documents), start=1
):
    print(f"{rank}. id={chunk_id} distance={distance:.4f} -> {chunk}")

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