# Summariser command-line tool in Python (RB-017)

Reads a text file or pasted text and prints a one-line headline and a bullet summary of a chosen length. Refuses input over a size limit and splits long text into parts.

| File | What it does |
| --- | --- |
| `summarize.py` | The tool (calls the Anthropic API) |
| `article.txt` | Made-up short news item |
| `long.txt` | Made-up longer item that needs 3 parts |
| `steps.json` | The steps the evidence runner replays |
| `article.src.md`, `article.md` | Tutorial source and built article |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python summarize.py article.txt --dry-run
python summarize.py long.txt --max-input 2000
cp .env.example .env   # then put your key in .env
set -a; source .env; set +a
python summarize.py article.txt --length short
python summarize.py long.txt --length long
echo "Some pasted text" | python summarize.py -
```

Model replies differ from run to run.
