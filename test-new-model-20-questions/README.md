# Test a new model with your own 20 questions (TT-022)

Asks 20 questions with checkable answers to two Claude models, scores the replies by a fixed rule, and records cost and time.

| File | What it is |
|---|---|
| `questions.json` | The 20 questions and the accepted answers |
| `models.py` | The two models and their prices per million tokens |
| `run_eval.py` | Asks every question to both models, saves `results.json` |
| `score.py` | The scoring rule and the report. No model involved |
| `test_score.py` | Checks the scoring rule on fixed answers, no API call |
| `spend_log.py` | Budget helper: one line per API call in `spend.log` |
| `steps.json` | The steps the runner replays |
| `article.src.md`, `article.md` | The tutorial |

Run (after `python3 -m venv .venv`, activating it, and `pip install -r requirements.txt`; put your key in `.env`
from `.env.example`, then `set -a; source .env; set +a`):

    python test_score.py
    python run_eval.py
    python score.py
