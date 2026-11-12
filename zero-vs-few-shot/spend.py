"""Add up spend.log. Prices are dollars per million tokens for the demo model."""
INPUT_PER_M, OUTPUT_PER_M = 0.10, 0.50  # check the provider's price page before you rely on these

calls = tin = tout = 0
for line in open("spend.log"):
    parts = dict(p.split("=") for p in line.split()[2:])
    calls += 1
    tin += int(parts["in"])
    tout += int(parts["out"])
cost = tin * INPUT_PER_M / 1e6 + tout * OUTPUT_PER_M / 1e6
print(f"Calls: {calls}")
print(f"Input tokens: {tin}")
print(f"Output tokens: {tout}")
print(f"Estimated cost: ${cost:.5f}")
