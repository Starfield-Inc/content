"""Read settings from the .env file, if there is one."""
from pathlib import Path


def load_env(path=".env"):
    """Return the NAME=value lines of a .env file as a dict. A missing file gives an empty dict."""
    settings = {}
    file = Path(path)
    if not file.is_file():
        return settings
    for line in file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            name, value = line.split("=", 1)
            settings[name.strip()] = value.strip()
    return settings
