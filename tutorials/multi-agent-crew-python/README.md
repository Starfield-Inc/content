# Three-role agent pipeline with CrewAI (RB-032)

A researcher, a writer and a reviewer hand work to each other using CrewAI and `claude-haiku-5-5`, with telemetry switched off and caps on iterations and tokens.

| File | What it does |
| --- | --- |
| `crew_run.py` | The three agents, three tasks and the crew (calls the Anthropic API) |
| `telemetry_check.py` | Confirms CrewAI telemetry is disabled |
| `requirements.txt` | `crewai[anthropic]`. Large install: 140 packages, 872M venv |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | The tutorial source and the built article |

Needs Python 3.10 to 3.13 (not 3.14) and `ANTHROPIC_API_KEY`.

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python telemetry_check.py
python crew_run.py
```
