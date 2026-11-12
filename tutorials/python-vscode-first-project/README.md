# Python in VS Code: first project

A beginner project: virtual environment, interpreter setting, one `claude-haiku-5-5` call, a launch config and a breakpoint check.

| File | What it does |
| --- | --- |
| `hello_haiku.py` | Makes one model call |
| `.vscode/settings.json` | Points VS Code at `.venv` |
| `.vscode/launch.json` | Debug configuration for F5 |
| `check_launch.py` | Checks both JSON files |
| `debug_check.py` | Stops at a breakpoint using debugpy |

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key_here" > .env
python hello_haiku.py
python debug_check.py
```

The VS Code window steps were described but not run.
