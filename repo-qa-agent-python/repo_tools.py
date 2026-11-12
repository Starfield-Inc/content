"""Read-only tools for the agent. Every path is checked against one repo folder."""
from pathlib import Path

MAX_FILE_CHARS = 4000
MAX_MATCHES = 20


class RefusedPath(Exception):
    """Raised when a path points outside the repo folder."""


class RepoTools:
    def __init__(self, repo):
        self.root = Path(repo).resolve()

    def _safe(self, relative):
        """Resolve a path (following symlinks) and refuse it if it leaves the repo folder."""
        target = (self.root / relative).resolve()
        if not target.is_relative_to(self.root):
            raise RefusedPath(f"refused: '{relative}' is outside the repo folder")
        return target

    def _files(self):
        return sorted(
            p for p in self.root.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.resolve().is_relative_to(self.root)
        )

    def list_files(self):
        return "\n".join(str(p.relative_to(self.root)) for p in self._files())

    def read_file(self, path):
        target = self._safe(path)
        if not target.is_file():
            return f"error: '{path}' is not a file in the repo"
        text = target.read_text(errors="replace")
        if len(text) > MAX_FILE_CHARS:
            text = text[:MAX_FILE_CHARS] + "\n[truncated]"
        return text

    def search_text(self, query):
        matches = []
        for p in self._files():
            for number, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
                if query.lower() in line.lower():
                    matches.append(f"{p.relative_to(self.root)}:{number}: {line.strip()}")
                    if len(matches) >= MAX_MATCHES:
                        return "\n".join(matches)
        return "\n".join(matches) or "no matches"

    def run(self, name, args):
        """Run one tool by name. Errors come back as text so the model can read them."""
        try:
            if name == "list_files":
                return self.list_files()
            if name == "read_file":
                return self.read_file(args["path"])
            if name == "search_text":
                return self.search_text(args["query"])
            return f"error: unknown tool '{name}'"
        except RefusedPath as err:
            return str(err)


TOOL_SCHEMAS = [
    {"name": "list_files", "description": "List every file in the repo folder.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "read_file", "description": "Read one text file. The path is relative to the repo folder.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "search_text", "description": "Find lines containing a word or phrase. Returns file:line: text.",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
]
