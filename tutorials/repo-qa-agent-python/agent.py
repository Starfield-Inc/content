import os
import sys

from anthropic import Anthropic

from repo_tools import TOOL_SCHEMAS, RepoTools

MODEL = os.environ.get("TUTORIAL_MODEL", "claude-haiku-5-5")
MAX_TOKENS = 2000
MAX_TURNS = 8
SYSTEM = (
    "You answer questions about a small code repository using the tools. "
    "Look at the files before you answer. Name the file paths your answer comes from. "
    "Keep answers under five sentences."
)
GUARD = " You can only read inside the repo; say so if asked for anything else."


def text_of(content):
    return "".join(block.text for block in content if block.type == "text")


def ask(client, tools, question, system):
    messages = [{"role": "user", "content": question}]
    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS, system=system, tools=TOOL_SCHEMAS, messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return text_of(response.content)
        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = tools.run(block.name, block.input)
                args = ", ".join(f"{k}={v!r}" for k, v in block.input.items())
                print(f"[tool] {block.name}({args}) -> {output.splitlines()[0][:70] if output else ''}")
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})
        messages.append({"role": "user", "content": results})
    return "[stopped: too many tool calls]"


def main():
    args = sys.argv[1:]
    no_guard = "--no-guard" in args
    args = [a for a in args if a != "--no-guard"]
    if not args:
        sys.exit('usage: python agent.py [--no-guard] "your question"')
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    print(f"you> {args[0]}")
    system = SYSTEM if no_guard else SYSTEM + GUARD
    answer = ask(Anthropic(), RepoTools("sample_repo"), args[0], system)
    print(f"agent> {answer}")


main()
