"""Math MCP server: simple arithmetic tools exposed over stdio."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math-server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the given exponent."""
    return base**exponent


if __name__ == "__main__":
    mcp.run(transport="stdio")
