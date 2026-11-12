# Jupyter setup and headless notebook run

Sets up Jupyter in a virtual environment, runs a notebook that asks `claude-haiku-5-5` to label eight sentences and charts the counts, then runs it headless with `nbconvert`.

| File | What it does |
| --- | --- |
| `requirements.txt` | Packages to install |
| `cells/` | The three code cells, one file each |
| `build_notebook.py` | Assembles `first_notebook.ipynb` from `cells/` |
| `show_outputs.py` | Prints the text outputs saved in an executed notebook |

Run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python build_notebook.py
jupyter nbconvert --to notebook --execute first_notebook.ipynb --output executed.ipynb
python show_outputs.py executed.ipynb
```
