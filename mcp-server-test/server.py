"""A small MCP server with three safe tools. It reads no files and uses no network or shell."""
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

MAX_CHARS = 1_000_000

mcp = MCPServer("labs-demo")


@mcp.tool()
def word_count(text: str) -> dict[str, int]:
    """Count the words, characters and lines in a piece of text."""
    if len(text) > MAX_CHARS:
        raise ToolError(f"text is {len(text)} characters, the limit is {MAX_CHARS}")
    return {"words": len(text.split()), "characters": len(text), "lines": len(text.splitlines())}


FACTORS = {"km_to_miles": 0.621371, "miles_to_km": 1.609344, "kg_to_lb": 2.204623, "lb_to_kg": 0.453592}


@mcp.tool()
def convert_units(value: float, conversion: str) -> float:
    """Convert a number. conversion is one of: km_to_miles, miles_to_km, kg_to_lb, lb_to_kg, c_to_f, f_to_c."""
    if conversion == "c_to_f":
        return round(value * 9 / 5 + 32, 2)
    if conversion == "f_to_c":
        return round((value - 32) * 5 / 9, 2)
    if conversion not in FACTORS:
        raise ToolError(f"unknown conversion '{conversion}'")
    return round(value * FACTORS[conversion], 2)


@mcp.tool()
def slugify(title: str) -> str:
    """Turn a title into a lower-case, hyphenated web address part."""
    words = "".join(c.lower() if c.isalnum() else " " for c in title).split()
    return "-".join(words)


if __name__ == "__main__":
    mcp.run()  # stdio is the default transport
