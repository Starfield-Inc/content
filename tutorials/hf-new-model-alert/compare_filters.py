"""Count what each candidate rule would drop for several organisations. Read-only, 7 API calls."""
import sys

from filters import RULES
from hfapi import newest_models

ORGS = ["Qwen", "google", "mistralai", "deepseek-ai", "microsoft", "meta-llama", "unsloth"]


def main():
    names = list(RULES)
    print(f"{'organisation':<13}{'fetched':>8}" + "".join(f"{n:>26}" for n in names))
    totals = {n: 0 for n in names}
    fetched_total = 0
    for org in ORGS:
        models, _ = newest_models(org, limit=40)
        counts = {n: sum(RULES[n](m, org) for m in models) for n in names}
        fetched_total += len(models)
        for n in names:
            totals[n] += counts[n]
        print(f"{org:<13}{len(models):>8}" + "".join(f"{counts[n]:>26}" for n in names))
    print(f"{'all':<13}{fetched_total:>8}" + "".join(f"{totals[n]:>26}" for n in names))
    print("\nEach number is how many of the newest 40 models the rule would drop.")


if __name__ == "__main__":
    sys.exit(main())
