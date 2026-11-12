"""Find the sentences closest in meaning to a question.

Usage: python search.py "your question" [--top 3]
"""
import argparse
import sys
from pathlib import Path

import numpy as np

from common import MODEL_NAME, cosine, embed, load_model, load_sentences

parser = argparse.ArgumentParser()
parser.add_argument("question")
parser.add_argument("--top", type=int, default=3)
parser.add_argument("--min-score", type=float, default=None, help="hide matches below this score")
args = parser.parse_args()

if not Path("vectors.npy").exists():
    print("Cannot find vectors.npy. Run python embed_sentences.py first.", file=sys.stderr)
    sys.exit(2)

sentences = load_sentences()
vectors = np.load("vectors.npy")
if len(vectors) != len(sentences):
    print("vectors.npy does not match sentences.txt. Run embed_sentences.py again.", file=sys.stderr)
    sys.exit(2)

model = load_model()
question_vector = embed(model, [args.question])[0]

scores = [cosine(question_vector, v) for v in vectors]
order = np.argsort(scores)[::-1][: args.top]

print(f"Question: {args.question}")
print(f"Model: {MODEL_NAME}")
shown = 0
for i in order:
    if args.min_score is not None and scores[i] < args.min_score:
        break
    shown += 1
    print(f"{shown}. {scores[i]:.3f}  {sentences[i]}")
if shown == 0:
    print(f"No sentence scored {args.min_score} or higher.")
