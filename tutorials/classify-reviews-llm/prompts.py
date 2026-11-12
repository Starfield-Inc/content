"""The two prompts the tutorial compares. {review} is filled in for each review."""

PROMPT_V1 = (
    "Label this review as positive, negative or mixed. Answer with one word.\n"
    "Review: {review}"
)

PROMPT_V2 = (
    "Label this review. Answer with one word: positive, negative or mixed.\n"
    "positive: the writer is happy overall.\n"
    "negative: the writer is unhappy overall. Praise words used as a joke still count as negative.\n"
    "mixed: clear good and bad points, or no strong opinion either way.\n"
    "Review: {review}"
)

PROMPTS = {"v1": PROMPT_V1, "v2": PROMPT_V2}
LABELS = ("positive", "negative", "mixed")
