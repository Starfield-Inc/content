# Hackathon pitch deck from a README

Builds a five-slide pitch deck (problem, demo, how it works, what is next, team) from the sections of a project README. A model call tightens the README text into slide text and speaker notes. A small script then checks that the talk fits a time limit.

| File | What it does |
| --- | --- |
| `sample-repo/` | The example project the deck is built from: README, demo script, notes file |
| `readme_parts.py` | Splits a README into its sections and reads the `Flow:` line for the picture |
| `build_deck.py` | Calls the model once, then writes `deck/index.html` and `deck/deck.json` |
| `timing.py` | Adds up speaker-note time and fails if the talk runs over |
| `steps.json` | The steps the evidence runner replays |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your key in .env, and load it into your shell
(cd sample-repo && python demo.py notes.txt)
python readme_parts.py sample-repo
python build_deck.py sample-repo demo.png deck   # demo.png: a screenshot of your demo
python -m http.server 8000 --directory deck      # open http://127.0.0.1:8000/
python timing.py deck/deck.json --limit 180
```

The model's wording differs on every run. The people in the sample README are made up.
