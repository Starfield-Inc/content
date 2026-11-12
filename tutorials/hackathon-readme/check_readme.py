"""Check a hackathon README against a seven-point checklist.

Usage: python check_readme.py path/to/README.md
Exit code 0 if every check passes, 1 if any fails, 2 if the file is missing.
"""
import re
import sys
from pathlib import Path

MIN_OPENING_WORDS = 6
MAX_OPENING_WORDS = 25
MAX_RUN_LINES = 3
DEMO_WITHIN_LINES = 12


def sections(lines):
    """Map each lowercase heading to the lines under it."""
    found, current = {}, None
    for line in lines:
        if m := re.match(r"^#{2,3}\s+(.*)", line):
            current = m.group(1).strip().lower()
            found[current] = []
        elif current:
            found[current].append(line)
    return found


def find_section(secs, *words):
    for name, body in secs.items():
        if any(w in name for w in words):
            return body
    return None


def opening_sentence(lines):
    """First paragraph of text after the title."""
    para = []
    for line in lines[1:]:
        if line.startswith("#"):
            if para:
                break
            continue
        if line.strip():
            para.append(line.strip())
        elif para:
            break
    return " ".join(para)


def run_block_lines(body):
    in_fence, cmds = False, []
    for line in body:
        if line.strip().startswith("```"):
            if in_fence:
                return cmds
            in_fence = True
        elif in_fence and line.strip():
            cmds.append(line.strip())
    return cmds if cmds else None


def check(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    secs = sections(lines)
    results = []

    opening = opening_sentence(lines)
    words = len(opening.split())
    ok = MIN_OPENING_WORDS <= words <= MAX_OPENING_WORDS and opening.count(". ") == 0
    results.append((ok, "Opens with one short sentence",
                    f"{words} words (want {MIN_OPENING_WORDS} to {MAX_OPENING_WORDS})" if words else "no opening line"))

    top = "\n".join(lines[:DEMO_WITHIN_LINES])
    demo = re.search(r"\[[^\]]*demo[^\]]*\]\(https?://[^)]+\)", top, re.I)
    results.append((bool(demo), "Demo link near the top", f"found in the first {DEMO_WITHIN_LINES} lines" if demo else f"no link with demo in its text in the first {DEMO_WITHIN_LINES} lines"))

    img = re.search(r"!\[[^\]]*\]\(([^)]+)\)", text)
    img_ok = bool(img) and (img.group(1).startswith("http") or (path.parent / img.group(1)).is_file())
    results.append((img_ok, "Screenshot that exists", img.group(1) if img else "no image found"))

    run = find_section(secs, "run")
    cmds = run_block_lines(run) if run else None
    results.append((bool(cmds) and len(cmds) <= MAX_RUN_LINES, "Run guide of three lines or fewer",
                    f"{len(cmds)} command lines" if cmds else "no code block under a Run heading"))

    tech = find_section(secs, "built with", "tech")
    results.append((bool(tech and any(l.strip().startswith(("-", "*")) for l in tech)),
                    "Tech list", "bullet list found" if tech else "no Built with heading"))

    nxt = find_section(secs, "next")
    results.append((bool(nxt and "".join(nxt).strip()), "What is next", "section found" if nxt else "no Next heading"))

    team = find_section(secs, "team")
    results.append((bool(team and "".join(team).strip()), "Team", "section found" if team else "no Team heading"))
    return results


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python check_readme.py path/to/README.md")
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Cannot find {path}")
        sys.exit(2)
    results = check(path)
    print(f"Checking {path}")
    for ok, name, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")
    passed = sum(ok for ok, _, _ in results)
    print(f"{passed} of {len(results)} checks passed")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
