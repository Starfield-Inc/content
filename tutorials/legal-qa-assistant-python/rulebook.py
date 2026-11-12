import re
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "are", "at", "be", "by", "can", "do", "does", "for", "from", "how",
    "i", "if", "in", "is", "it", "many", "may", "me", "much", "my", "of", "on", "or",
    "the", "to", "what", "when", "who", "will", "with", "you", "must", "much", "long",
}


def load_rules(path="rules.txt"):
    """Return {rule number: text}. Each line is 'Rule N. text'."""
    rules = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        match = re.match(r"Rule (\d+)\. (.+)", line.strip())
        if match:
            rules[int(match.group(1))] = match.group(2)
    return rules


def words(text):
    found = re.findall(r"[a-z]+", text.lower())
    return {w.rstrip("s") for w in found if w not in STOPWORDS and len(w) > 2}


def retrieve(question, rules, top=3):
    """Score each rule by the question words it shares, so a word found in few rules counts more."""
    asked = words(question)
    rule_words = {number: words(text) for number, text in rules.items()}
    scored = []
    for number, found in rule_words.items():
        score = sum(1 / sum(w in other for other in rule_words.values()) for w in asked & found)
        scored.append((score, number))
    scored = [item for item in sorted(scored, key=lambda s: (-s[0], s[1])) if item[0] > 0]
    return [number for _, number in scored[:top]]


if __name__ == "__main__":
    import sys

    rules = load_rules()
    print(f"{len(rules)} rules loaded")
    question = " ".join(sys.argv[1:])
    if question:
        print(f"question: {question}")
        print("retrieved:", retrieve(question, rules) or "nothing")
