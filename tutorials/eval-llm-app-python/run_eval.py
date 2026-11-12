"""Run every case in cases.json through the app and score each reply by rule."""
import argparse
import json
import sys
import time
from pathlib import Path

from app import reply


def check(case, text):
    """Return a list of reasons the reply fails. An empty list means it passed."""
    problems = []
    low = text.lower()
    if not text:
        return ["empty reply"]
    for options in case.get("must_include", []):
        if not any(o.lower() in low for o in options):
            problems.append("missing one of: " + " | ".join(options))
    for bad in case.get("must_not_include", []):
        if bad.lower() in low:
            problems.append(f"contains forbidden text: {bad}")
    limit = case.get("max_words")
    if limit and len(text.split()) > limit:
        problems.append(f"{len(text.split())} words, limit {limit}")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="v1", help="which prompt in app.py to test")
    parser.add_argument("--out", help="save results to this JSON file")
    parser.add_argument("--only", nargs="*", help="run only these case ids")
    parser.add_argument("--fail-under", type=float, default=0, help="exit 1 if the pass rate is below this percent")
    args = parser.parse_args()

    cases = json.loads(Path("cases.json").read_text())
    if args.only:
        cases = [c for c in cases if c["id"] in args.only]
    results = []
    for case in cases:
        text = reply(case["message"], args.prompt)
        problems = check(case, text)
        results.append({"id": case["id"], "passed": not problems, "problems": problems, "reply": text})
        print(f"{'PASS' if not problems else 'FAIL'}  {case['id']}")
        time.sleep(0.2)

    passed = sum(r["passed"] for r in results)
    rate = 100 * passed / len(results)
    print(f"\nprompt {args.prompt}: {passed}/{len(results)} passed, pass rate {rate:.0f}%")
    failed = [r["id"] for r in results if not r["passed"]]
    print("failed: " + (", ".join(failed) if failed else "none"))
    if args.out:
        Path(args.out).parent.mkdir(exist_ok=True)
        Path(args.out).write_text(json.dumps({"prompt": args.prompt, "pass_rate": rate, "results": results}, indent=1))
    if rate < args.fail_under:
        sys.exit(1)


if __name__ == "__main__":
    main()
