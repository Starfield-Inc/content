"""Check .vscode/launch.json and settings.json: valid JSON, and the program file exists."""
import json
import sys
from pathlib import Path

root = Path(__file__).parent
settings = json.loads((root / ".vscode/settings.json").read_text())
launch = json.loads((root / ".vscode/launch.json").read_text())
print("settings.json: valid JSON, interpreter =", settings["python.defaultInterpreterPath"])
for cfg in launch["configurations"]:
    program = Path(cfg["program"].replace("${workspaceFolder}", str(root)))
    print(f"launch.json: '{cfg['name']}' type={cfg['type']} program exists={program.is_file()}")
    if not program.is_file():
        sys.exit(1)
