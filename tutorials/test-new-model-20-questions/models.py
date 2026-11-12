"""The two models and their prices in US dollars per million tokens.
Check the provider's pricing page before you rely on these numbers."""

MODELS = {
    # "thinking" is how each model is told not to think before it answers. The two models name it differently.
    "claude-haiku-5-5": {"label": "Haiku 5.5", "input": 0.10, "output": 0.50, "thinking": {"type": "disabled"}},
    "claude-sonnet-5-5": {"label": "Sonnet 5.5", "input": 2.00, "output": 10.00, "thinking": {"type": "between_tools"}},
}
MAX_TOKENS = 200


def cost_usd(model, input_tokens, output_tokens):
    price = MODELS[model]
    return (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
