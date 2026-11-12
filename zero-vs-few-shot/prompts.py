LABELS = ["HIGH", "MEDIUM", "LOW"]

INSTRUCTION = "Label this customer message with a priority: HIGH, MEDIUM or LOW. Reply with the label only."

# Three examples, one per label. None of them is in inputs.csv.
EXAMPLES = [
    ("I paid for the yearly plan but my account still says Free and I cannot open my projects.", "HIGH"),
    ("The calendar shows the wrong time zone for new events, though I can edit each one.", "MEDIUM"),
    ("Does the team plan include extra storage?", "LOW"),
]


def build_prompt(mode, text):
    """mode is "zero" (no examples) or "few" (the three examples above)."""
    parts = [INSTRUCTION]
    if mode == "few":
        for example_text, label in EXAMPLES:
            parts.append(f"Message: {example_text}\nPriority: {label}")
    parts.append(f"Message: {text}\nPriority:")
    return "\n\n".join(parts)
