"""No API call. Fixed strings show what the schema accepts and rejects."""
from ask_json import check

CASES = {
    "valid": '{"category": "bug", "priority": 3, "summary": "Export button does nothing", "needs_human": true}',
    "word instead of number": '{"category": "bug", "priority": "high", "summary": "Export button does nothing", "needs_human": true}',
    "category not allowed": '{"category": "feature_request", "priority": 2, "summary": "Add dark mode please", "needs_human": false}',
    "code fence around JSON": '```json\n{"category": "bug", "priority": 3, "summary": "Export button does nothing", "needs_human": true}\n```',
    "missing key": '{"category": "bug", "priority": 3, "summary": "Export button does nothing"}',
    "empty reply": "",
}

for label, raw in CASES.items():
    ticket, error = check(raw)
    print(f"{label}: {'ACCEPTED' if ticket else 'REJECTED'}")
    if error:
        print("   ", error)
