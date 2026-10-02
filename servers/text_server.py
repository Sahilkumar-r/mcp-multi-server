"""Text MCP server: simple string utilities exposed over stdio."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("text-server")


@mcp.tool()
def word_count(text: str) -> int:
    """Count the words in a piece of text."""
    return len(text.split())


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


@mcp.tool()
def to_upper(text: str) -> str:
    """Convert text to upper case."""
    return text.upper()


if __name__ == "__main__":
    mcp.run(transport="stdio")
