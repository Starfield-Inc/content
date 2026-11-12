"""Shared helpers: load the embedding model, read the sentences, compare vectors."""
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"
HERE = Path(__file__).parent
SENTENCES_FILE = HERE / "sentences.txt"
MODEL_DIR = HERE / "models"  # the model is downloaded here once


def load_model():
    return TextEmbedding(model_name=MODEL_NAME, cache_dir=str(MODEL_DIR))


def load_sentences():
    lines = SENTENCES_FILE.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def embed(model, texts):
    """Return an array with one row per text."""
    return np.array(list(model.embed(texts)))


def cosine(a, b):
    """Cosine similarity: 1.0 means the same direction, 0 means unrelated."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
