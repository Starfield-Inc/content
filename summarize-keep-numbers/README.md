# Summarise a long text and keep the numbers (TT-025)

Splits a long text into chunks, summarises each chunk with an LLM, merges the chunk summaries, then lists every number in the source and reports which ones the summary dropped or invented.

| File | What it does |
| --- | --- |
| `report.txt` | A made-up annual report with many numbers (written for this tutorial) |
| `bad_summary.txt` | A hand-written summary with a dropped number and a changed number, for the checker |
| `numcheck.py` | Extracts numbers from text and compares a source with a summary |
| `chunks.py` | Splits text on paragraph breaks into chunks of a set size |
| `summarize.py` | Chunk, summarise, merge, check (calls the Anthropic API) |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | The tutorial source and the built article |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python numcheck.py report.txt
python numcheck.py report.txt bad_summary.txt
python chunks.py report.txt
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python summarize.py report.txt
python summarize.py report.txt --words 50
```

`summarize.py` needs `ANTHROPIC_API_KEY`. Model replies differ from run to run, so the counts of kept and missing numbers differ too.
