"""The same server plus one tool nobody planned. Used to show the client catching it."""
from server import mcp


@mcp.tool()
def debug_dump() -> str:
    """Left in by mistake."""
    return "internal state"


if __name__ == "__main__":
    mcp.run()
