import sys
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

from ask_json import LOOSE, STRICT, ask_json, client_or_exit

MESSAGES = [
    "I was charged twice for May and I want one of the charges refunded today.",
    "The export button does nothing when I click it on Firefox. Started after the last update.",
    "Do you support single sign-on for teams? Thanks.",
    "Please add dark mode. It would be nice for night work.",
    "My invoice shows the wrong company name. Can you fix it before Friday?",
    "The app crashes every time I upload a file larger than 20 MB.",
    "How do I invite a colleague to my workspace?",
    "Could you add an option to export reports as PDF?",
    "I cancelled last month but my card was charged again this morning.",
    "Login page shows a blank screen on my phone since yesterday.",
]
RUNS = 50

name = sys.argv[1] if len(sys.argv) > 1 else "strict"
prompt = {"strict": STRICT, "loose": LOOSE}[name]
client = client_or_exit()


def one(i):
    return ask_json(client, prompt, MESSAGES[i % len(MESSAGES)], retries=1)


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(one, range(RUNS)))

first_try_ok = sum(1 for t, attempts, f in results if attempts == 1 and t)
fixed_by_retry = sum(1 for t, attempts, f in results if attempts == 2 and t)
still_bad = sum(1 for t, attempts, f in results if not t)
kinds = Counter()
for t, attempts, failures in results:
    if failures:
        # count which field names appear in the first failure
        for part in failures[0][1].split("; "):
            kinds[part.split(":")[0]] += 1

print(f"prompt: {name}   runs: {RUNS}")
print(f"valid on the first try:        {first_try_ok}")
print(f"invalid, valid after 1 retry:  {fixed_by_retry}")
print(f"invalid after the retry:       {still_bad}")
print(f"first-try failure rate:        {RUNS - first_try_ok} of {RUNS}")
print("fields that failed on the first try:", dict(kinds) or "none")
