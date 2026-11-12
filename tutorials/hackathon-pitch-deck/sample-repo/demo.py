import re
import sys
from collections import defaultdict

COMMIT = re.compile(r"^(?P<who>[A-Z][a-z]+)\s+(?:will|to do)\s+(?P<task>.+?)\.?$")


def find_actions(text):
    """Return {owner: [tasks]} for lines like 'Maya will update the page.'"""
    actions = defaultdict(list)
    for line in text.splitlines():
        match = COMMIT.match(line.strip())
        if match:
            actions[match["who"]].append(match["task"])
    return actions


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python demo.py notes.txt")
    for owner, tasks in find_actions(open(sys.argv[1]).read()).items():
        for task in tasks:
            print(f"{owner}: {task}")
