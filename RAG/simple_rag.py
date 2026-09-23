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

documents = [
    "Python is a dynamically typed programming language.",
    "PostgreSQL is a relational database management system.",
    "Docker packages applications and their dependencies into containers.",
    "Kubernetes is used to orchestrate and manage containers.",
    "Redis is an in-memory data store commonly used for caching."
]

# convert documents into embeddings

documentEmbeddings = embeddingModel.encode(documents)

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

for document, score in zip(documents, scores):
    print(f"{score: .4f} -> {document}")

# find most similar documents

bestMatchIndex=scores.argmax()

print("\n Best match : ")
print(documents[bestMatchIndex])
print('documentEmbeddings.shape', documentEmbeddings.shape)
query_embedding = embeddingModel.encode([query])
print('query_embedding.shape', query_embedding.shape)

top_k=3 # top k documents

top_indices = np.argsort(scores)[::-1][:top_k]

print("\n Top results:")

retreived_documents = []

for index in top_indices:
    retreived_documents.append(documents[index])
    print(f"{scores[index]:.4f}->{documents[index]}")

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

response = client.models.generate_content(
    model=gemini_model_name or '',
    contents=prompt,
)

print("\nLLM Answer: ")
print(response.text)