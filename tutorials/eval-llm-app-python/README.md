# Evaluate an LLM app with 20 test cases

A small support-reply app for a made-up tea shop, and an evaluation script that sends 20 test messages through it, checks each reply by rule and prints a pass rate. It shows one failing case, the prompt change that followed, and a run-to-run comparison.

| File | What it does |
| --- | --- |
| `app.py` | The app under test: `reply(message, prompt)` with two prompts, `v1` and `v2` |
| `cases.json` | The 20 test cases: a message and the rules its reply must meet |
| `run_eval.py` | Runs the cases, prints PASS or FAIL per case and the pass rate, saves results as JSON |
| `show_failures.py` | Prints the failing cases from a results file |
| `compare_runs.py` | Compares two results files case by case |
| `test_checks.py` | Tests the checker itself with fixed replies (no API call) |
| `.env.example` | Shows the variable name. Copy to `.env` and add your own key |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your key in .env
python -m unittest -v test_checks
python run_eval.py --prompt v1 --out results/v1.json
python show_failures.py results/v1.json
python run_eval.py --prompt v2 --out results/v2-a.json
python run_eval.py --prompt v2 --out results/v2-b.json
python compare_runs.py results/v2-a.json results/v2-b.json
```

Model replies differ from run to run, so your pass rates may differ from the article.
