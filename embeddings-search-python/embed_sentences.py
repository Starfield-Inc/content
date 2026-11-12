"""Embed every sentence once and save the vectors to vectors.npy."""
import time

import numpy as np

from common import MODEL_NAME, embed, load_model, load_sentences

start = time.time()
model = load_model()
print(f"Model: {MODEL_NAME} (loaded in {time.time() - start:.1f}s)")

sentences = load_sentences()
vectors = embed(model, sentences)
np.save("vectors.npy", vectors)

print(f"Sentences: {len(sentences)}")
print(f"Vector array shape: {vectors.shape}")
print(f"First sentence: {sentences[0]}")
first = ", ".join(f"{x:.3f}" for x in vectors[0][:5])
print(f"First 5 numbers: [{first}]")
