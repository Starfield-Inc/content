import json
import re
import sys

from rulebook import load_rules

CITATION = re.compile(r"\[Rule (\d+)\]")


def check(answer_text, rules):
    """Return (cited numbers, cited numbers missing from the rulebook, disclaimer present)."""
    cited = [int(n) for n in CITATION.findall(answer_text)]
    missing = sorted({n for n in cited if n not in rules})
    return cited, missing, "not legal advice" in answer_text


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "answers.log"
    try:
        lines = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    except FileNotFoundError:
        sys.exit(f"Cannot find {path}")
    rules = load_rules()
    print(f"Rulebook has {len(rules)} rules. Checking {len(lines)} answers in {path}.")
    failed = False
    for i, item in enumerate(lines, 1):
        cited, missing, disclaimer = check(item["answer"], rules)
        problems = []
        if missing:
            problems.append(f"quotes rule {', '.join(map(str, missing))} which is not in the rulebook")
        if not disclaimer:
            problems.append("has no disclaimer")
        status = "FAIL" if problems else "ok"
        failed = failed or bool(problems)
        print(f"answer {i}: cited {sorted(set(cited)) or 'none'} -> {status} {'; '.join(problems)}".rstrip())
    if failed:
        sys.exit(1)
    print("All quoted rule numbers exist and every answer has the disclaimer.")


if __name__ == "__main__":
    main()
