from ask_json import STRICT, ask_json, client_or_exit

MESSAGES = [
    "I was charged twice for May and I want one of the charges refunded today.",
    "The export button does nothing when I click it on Firefox. Started after the last update.",
    "Do you support single sign-on for teams? Thanks.",
    "Please add dark mode. It would be nice for night work.",
]
client = client_or_exit()
for text in MESSAGES:
    ticket, attempts, failures = ask_json(client, STRICT, text, retries=0)
    print("message:", text)
    print("  ", ticket.model_dump_json() if ticket else "INVALID: " + failures[0][1])
