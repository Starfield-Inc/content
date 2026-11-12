# Embeddings and semantic search

Embeds 20 short sentences with a small open model that runs on your own machine, then finds the sentences closest in meaning to a question. No API key is needed.

| File | What it does |
| --- | --- |
| `sentences.txt` | The 20 example sentences, one per line |
| `common.py` | Loads the model, reads the sentences, computes cosine similarity |
| `embed_sentences.py` | Embeds every sentence and saves `vectors.npy` |
| `compare.py` | Embeds one question and compares it with three sentences |
| `search.py` | Prints the top matches for a question |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python embed_sentences.py     # downloads the model (about 66 MB) on first run
python search.py "Where can I get a boat to the island?"
python search.py "What is the capital of France?" --min-score 0.5
```

Model: `BAAI/bge-small-en-v1.5` (MIT licence), run through `fastembed` (Apache-2.0) as a quantized ONNX build. It is downloaded into `models/` in this folder.
