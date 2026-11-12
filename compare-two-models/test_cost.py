from models import cost_usd

# 1,000,000 input tokens at the listed input price, and the same for output.
assert abs(cost_usd("claude-haiku-5-5", 1_000_000, 0) - 0.10) < 1e-9
assert abs(cost_usd("claude-haiku-5-5", 0, 1_000_000) - 0.50) < 1e-9
assert abs(cost_usd("claude-sonnet-5-5", 1_000_000, 0) - 2.00) < 1e-9
assert abs(cost_usd("claude-sonnet-5-5", 0, 1_000_000) - 10.00) < 1e-9
# A small call: 40 input and 60 output tokens on the second model.
assert abs(cost_usd("claude-sonnet-5-5", 40, 60) - 0.00068) < 1e-9
print("cost checks passed")
