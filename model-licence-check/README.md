# Check a model's licence with a script and a checklist

Reads the licence field of public Hugging Face models through the public API, fetches each licence file, flags lines that answer six checklist questions, and saves a short report. The script marks text for a person to read. It is not legal advice.

| File | What it does |
| --- | --- |
| `models.txt` | The models to check, one `publisher/name` per line |
| `hfapi.py` | Reads model records and raw files with a User-Agent and a pause |
| `checklist.py` | The six questions and the phrases that point to lines worth reading |
| `licence_check.py` | Fetch, check, print a summary, save `report.md` |
| `tests/test_checklist.py` | Checks the line splitting and the phrases on fixed text |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python licence_check.py --tags-only
python licence_check.py
```

`report.md` is ignored by git. Get a lawyer's view before you rely on a licence. Output depends on live data.
