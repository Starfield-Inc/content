# Zero-shot vs few-shot prompting

Labels 20 short customer messages as HIGH, MEDIUM or LOW priority with no examples, then with three, and scores both runs from the saved output. Tutorial TT-018.

The expected labels in `inputs.csv` follow one rule written by the author: HIGH when the customer cannot use the product or has lost money or data, MEDIUM when something works wrongly but the customer has a workaround, LOW for a question or a suggestion. The prompt does not state this rule; the three examples are the only place the model could learn it.

| File | What it does |
| --- | --- |
| `inputs.csv` | 20 messages written for this tutorial, with the expected label |
| `prompts.py` | The instruction, the three examples and `build_prompt` |
| `check_data.py` | Checks the data (no API call) |
| `run.py` | Sends the 20 inputs in one mode and saves the raw replies |
| `score.py` | Scores the saved replies and prints the failures |
| `spend_log.py`, `spend.py` | Budget helpers: one line per call in `spend.log`, and a total |
| `steps.json` | The steps the runner replays |

Run (after `python3 -m venv .venv` and activating it, with the key loaded):

```bash
pip install -r requirements.txt
python check_data.py
python run.py zero
python run.py few
python score.py
```

To use it in a notebook, paste `prompts.py` into one cell, `run.py` (without the last block) into a second, and `score.py` into a third.
