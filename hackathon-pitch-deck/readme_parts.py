import re
import sys
from pathlib import Path

WANTED = ["Problem", "Demo", "How it works", "What is next", "Team"]


def split_sections(markdown):
    """Return {heading: text} for every '## heading' in the README."""
    sections, name, lines = {}, None, []
    for line in markdown.splitlines():
        match = re.match(r"^##\s+(.*?)\s*$", line)
        if match:
            if name:
                sections[name] = "\n".join(lines).strip()
            name, lines = match.group(1), []
        elif name:
            lines.append(line)
    if name:
        sections[name] = "\n".join(lines).strip()
    return sections


def title_of(markdown):
    match = re.search(r"^#\s+(.*?)\s*$", markdown, re.M)
    return match.group(1) if match else "Untitled project"


def flow_of(text):
    """Pull the 'Flow: a -> b -> c' line out of a section and return the boxes."""
    match = re.search(r"^Flow:\s*(.+)$", text, re.M)
    return [part.strip() for part in match.group(1).split("->")] if match else []


if __name__ == "__main__":
    readme = Path(sys.argv[1]) / "README.md"
    if not readme.is_file():
        sys.exit(f"Cannot find {readme}")
    text = readme.read_text()
    found = split_sections(text)
    print(f"Project: {title_of(text)}")
    for name in WANTED:
        body = found.get(name)
        if body is None:
            print(f"{name:<13} MISSING - add a '## {name}' section to the README")
        else:
            print(f"{name:<13} {len(body.split()):>3} words")
    flow = flow_of(found.get("How it works", ""))
    print(f"Flow boxes: {len(flow)}" + (f" ({' > '.join(flow)})" if flow else ""))
    if any(name not in found for name in WANTED):
        sys.exit(1)
