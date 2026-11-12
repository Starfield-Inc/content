# Rulebook Q&A assistant with citations (RB-037)

Answers questions about an invented ten-rule rulebook with keyword retrieval and claude-haiku-5-5, cites the rule number, refuses advice requests, adds a disclaimer, and checks that every quoted rule exists. Legal must review before publishing. The rulebook is fiction.

| File | What it does |
| --- | --- |
| `rules.txt` | The invented rulebook |
| `rulebook.py` | Loads rules and retrieves matches by keyword |
| `ask.py` | Retrieve, ask the model, add the disclaimer, log the answer (calls the Anthropic API) |
| `verify.py` | Checks quoted rule numbers and disclaimers in a log |
| `bad_answers.log` | Two hand-written failing answers for the checker |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | The tutorial source and the built article |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python rulebook.py "How many witnesses can I bring to the hearing?"
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python ask.py "How many witnesses can I bring to the hearing?"
python ask.py "Should I sue my neighbour over the fence, and will I win?"
python verify.py
python verify.py bad_answers.log
```
