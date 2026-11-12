from ask_json import LOOSE, ask_json, client_or_exit

TEXT = "Do you support single sign-on for teams? Thanks."
client = client_or_exit()

print("message:", TEXT)
print("--- loose prompt, no retry ---")
ticket, attempts, failures = ask_json(client, LOOSE, TEXT, retries=0)
for raw, error in failures:
    print("raw reply:", raw)
    print("errors:", error)
print("result:", "valid" if ticket else "INVALID after", attempts, "attempt")

print("--- loose prompt, one retry with the error message ---")
ticket, attempts, failures = ask_json(client, LOOSE, TEXT, retries=1)
for raw, error in failures:
    print("attempt 1 raw reply:", raw)
    print("attempt 1 errors:", error)
print("result:", ("valid on attempt %d: " % attempts + ticket.model_dump_json()) if ticket else "INVALID after %d attempts" % attempts)
