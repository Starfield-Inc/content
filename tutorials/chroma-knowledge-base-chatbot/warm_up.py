"""Load Chroma's default embedding model. The first call downloads it, later calls reuse it."""
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

vectors = DefaultEmbeddingFunction()(["warm up"])
print(f"Model ready: all-MiniLM-L6-v2, vectors of {len(vectors[0])} numbers")
