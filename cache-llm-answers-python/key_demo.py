from llm_cache import MAX_TOKENS, MODEL, SYSTEM, make_key

Q = "What is a context window?"
base = make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, Q)
cases = {
    "same request again": make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, Q),
    "other model name": make_key("claude-sonnet-5-5", MAX_TOKENS, "disabled", SYSTEM, Q),
    "max_tokens 500": make_key(MODEL, 500, "disabled", SYSTEM, Q),
    "thinking enabled": make_key(MODEL, MAX_TOKENS, "enabled", SYSTEM, Q),
    "extra space inside": make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, "What is a  context window?"),
    "space at the end": make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, Q + " "),
    "lower case": make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, Q.lower()),
    "messy, normalize on": make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, "  What is a  context window? ", normalize=True),
    "tidy, normalize on": make_key(MODEL, MAX_TOKENS, "disabled", SYSTEM, Q, normalize=True),
}
print(f"base key: {base[:12]}")
for name, key in cases.items():
    verdict = "same key" if key == base else "NEW key"
    print(f"{name:22} {key[:12]}  {verdict}")
