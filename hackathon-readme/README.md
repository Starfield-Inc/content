# Hackathon README tutorial

A README checklist script, a before and after example, and a template for a hackathon project README. No API key needed.

| File | What it does |
| --- | --- |
| `check_readme.py` | Checks a README against seven points and exits 1 if any fail |
| `render_readme.py` | Renders a README to `site/index.html` to see it as a browser shows it |
| `template/README.template.md` | Fill-in template |
| `weak/README.md` | A typical weak README (fails all 7 checks) |
| `example/` | A tiny working project (`app.py`, `notes.txt`) with a README that passes |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python check_readme.py weak/README.md
python check_readme.py example/README.md
python render_readme.py example/README.md
```

The links in the example README (`example.com`) are placeholders. `example/screenshot.png` is the rendered image of `app.py`'s real output from one run.
