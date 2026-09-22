from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# loading embedding model

embeddingModel = SentenceTransformer("all-MiniLM-L6-v2")

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

query = "Which technology is used to manage containers?"

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

for index in top_indices:
    print(f"{scores[index]:.4f}->{documents[index]}")

    