import json
from pathlib import Path

DEFAULT_PATH = Path("books.json")


def load_books(path=DEFAULT_PATH):
    """Return the list of books, or an empty list if the file does not exist."""
    if not Path(path).exists():
        return []
    return json.loads(Path(path).read_text())


def save_books(books, path=DEFAULT_PATH):
    """Write the list of books to disk as JSON."""
    Path(path).write_text(json.dumps(books, indent=2))
