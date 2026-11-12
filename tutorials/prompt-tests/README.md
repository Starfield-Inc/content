# Prompts as tests

Five prompts, each with a test that checks the answer by rule: expected facts, format and length. A sixth file changes one prompt so you can watch a check fail.

| File | What it does |
| --- | --- |
| `prompts.py` | The five prompts |
| `prompts_changed.py` | The same prompts with the summary prompt changed |
| `llm.py` | Sends a prompt, returns the text, logs tokens to `spend.log` |
| `test_prompts.py` | The five tests (standard library `unittest`) |
| `ask.py` | Sends one prompt: `python ask.py capital` |
| `spend.py` | Adds up `spend.log` |
| `.env.example` | Shows the variable name. Copy to `.env` and add your own key |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your key in .env
python -m unittest -v test_prompts
PROMPTS_MODULE=prompts_changed python -m unittest -v test_prompts
```
