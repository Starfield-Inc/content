"""Start an MCP server over stdio, connect to it, and print a pass or fail checklist.

Usage: python test_client.py [server_file]
"""
import asyncio
import sys
import time

from mcp import Client, StdioServerParameters

EXPECTED_TOOLS = {"word_count", "convert_units", "slugify"}
TIME_LIMIT = 5.0
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))


def text_of(result):
    return " ".join(block.text for block in result.content if block.type == "text")


async def main(server_file):
    params = StdioServerParameters(command=sys.executable, args=[server_file])
    async with Client(params, read_timeout_seconds=TIME_LIMIT) as client:
        check("connected to the server over stdio", True)

        tools = (await client.list_tools()).tools
        names = {t.name for t in tools}
        print("      tools listed:", ", ".join(sorted(names)))
        check("all three expected tools are listed", EXPECTED_TOOLS <= names)
        check("no tool we did not intend is exposed", names <= EXPECTED_TOOLS,
              f"unexpected: {sorted(names - EXPECTED_TOOLS)}" if names - EXPECTED_TOOLS else "")
        check("every tool has a description", all(t.description for t in tools))

        r = await client.call_tool("word_count", {"text": "one two three\nfour"})
        check("word_count returns 4 words", not r.is_error and r.structured_content["words"] == 4,
              str(r.structured_content))

        r = await client.call_tool("convert_units", {"value": 100, "conversion": "c_to_f"})
        check("convert_units turns 100 C into 212 F", not r.is_error and r.structured_content["result"] == 212,
              text_of(r))

        r = await client.call_tool("slugify", {"title": "Test an MCP Server!"})
        check("slugify returns test-an-mcp-server", text_of(r) == "test-an-mcp-server", text_of(r))

        r = await client.call_tool("convert_units", {"value": "abc", "conversion": "c_to_f"})
        check("bad input comes back as an error result, not a crash", r.is_error,
              text_of(r).splitlines()[0])

        r = await client.call_tool("convert_units", {"value": 1, "conversion": "parsecs"})
        check("a bad value is explained in the error text", r.is_error and "unknown conversion" in text_of(r),
              text_of(r))

        r = await client.call_tool("no_such_tool", {})
        check("an unknown tool name is an error result", r.is_error, text_of(r))

        start = time.monotonic()
        try:
            r = await client.call_tool("word_count", {"text": "x " * 2_500_000})
            outcome = "error result" if r.is_error else "answered"
        except TimeoutError:
            outcome = "timed out"
        took = time.monotonic() - start
        check(f"a 5 million character input ends within {TIME_LIMIT:.0f} seconds", took < TIME_LIMIT,
              f"{outcome} in {took:.2f} s")

        r = await client.call_tool("slugify", {"title": "Still alive"})
        check("the server still answers after the huge call", text_of(r) == "still-alive", text_of(r))


try:
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "server.py"))
except Exception as exc:
    while hasattr(exc, "exceptions"):
        exc = exc.exceptions[0]
    check("the run finished without an exception", False, f"{type(exc).__name__}: {exc}")

print(f"\n{sum(results)} of {len(results)} checks passed")
sys.exit(0 if all(results) else 1)
