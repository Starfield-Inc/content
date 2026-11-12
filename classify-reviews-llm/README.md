# Classify reviews with an LLM and check the result

Labels 50 short reviews with one API call each, then counts right and wrong against labels you wrote.

| File | What it does |
| --- | --- |
| `reviews.csv` | 50 original reviews with a label column |
| `prompts.py` | The two prompts (v1 and v2) |
| `classify.py` | Calls the model once per review and saves `results_<prompt>.csv` |
| `score.py` | Counts right and wrong and lists the wrong ones |
| `check_data.py` | Counts the labels in `reviews.csv` |
| `spend.py` | Adds up `spend.log` (one line per call) |
| `.env.example` | Shows the variable name. Copy to `.env` and add your own key |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your key in .env
python classify.py --prompt v1
python score.py results_v1.csv
```
