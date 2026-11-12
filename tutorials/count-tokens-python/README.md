# Token counter

Counts the tokens in a text file with `tiktoken`, for two encodings, and can turn the count into a cost estimate from a price you type in.

| File | What it does |
| --- | --- |
| `tokens_demo.py` | Shows how one sentence splits into tokens |
| `count_tokens.py` | Counts the tokens in a file and optionally estimates cost |
| `sample.txt` | A sample text to count |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tokens_demo.py "Tokens are not the same as words."
python count_tokens.py sample.txt --price-per-million 3.00
```

The price in the example is a made-up number. Copy the real input price from your provider's price page on the day you run it.
