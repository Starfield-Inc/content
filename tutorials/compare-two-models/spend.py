"""Add up spend.log by model. Prices come from models.py."""
from models import MODELS, cost_usd

totals = {}
for line in open("spend.log"):
    parts = dict(p.split("=") for p in line.split()[2:])
    t = totals.setdefault(parts["model"], [0, 0, 0])
    t[0] += 1
    t[1] += int(parts["in"])
    t[2] += int(parts["out"])
total = 0.0
for model, (calls, tin, tout) in totals.items():
    cost = cost_usd(model, tin, tout)
    total += cost
    print(f"{model}: {calls} calls, {tin} input tokens, {tout} output tokens, ${cost:.5f}")
print(f"Total: ${total:.5f}")
