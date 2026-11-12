"""Rules that decide whether a model is a copy or a variant of someone else's model.

The Hub writes a tag such as  base_model:quantized:mistralai/Mistral-Large-4-1T-A52B
(or base_model:finetune:..., base_model:adapter:..., base_model:merge:...).
Older cards only have the short form  base_model:owner/name.
"""
from datetime import datetime, timedelta, timezone


def parse_created(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def in_window(model, days, now=None):
    now = now or datetime.now(timezone.utc)
    return parse_created(model["createdAt"]) >= now - timedelta(days=days)


def base_models(model):
    """List of (relation, owner/name) pairs from the base_model tags. Relation is '' for the short form."""
    found = []
    for tag in model.get("tags", []):
        if not tag.startswith("base_model:"):
            continue
        parts = tag.split(":", 2)[1:]
        found.append(("", parts[0]) if len(parts) == 1 else (parts[0], parts[1]))
    return found


# Each rule answers: should this model be dropped? Used by compare_filters.py to test them side by side.
def rule_not_open_access(model, org):
    return bool(model.get("gated"))


def rule_any_base_model(model, org):
    return bool(base_models(model))


def rule_other_author_base(model, org):
    """Built on a model that another author owns: a copy, a quantised upload or a fine-tune of theirs."""
    return any(not name.startswith(org + "/") for _, name in base_models(model))


def rule_file_format_name(model, org):
    name = model["id"].lower()
    return any(word in name for word in ("gguf", "-awq", "-gptq", "-bnb", "-mlx"))


RULES = {
    "gated": rule_not_open_access,
    "any base_model": rule_any_base_model,
    "other-author base_model": rule_other_author_base,
    "format in name": rule_file_format_name,
}

CHOSEN = rule_other_author_base
