"""MCP client that connects to both servers, lists their tools and calls them."""
import asyncio
import json
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).parent
SERVERS = {
    "math": ROOT / "servers" / "math_server.py",
    "text": ROOT / "servers" / "text_server.py",
}


class MultiServerClient:
    def __init__(self):
        self.stack = AsyncExitStack()
        self.sessions: dict[str, ClientSession] = {}
        self.tool_to_server: dict[str, str] = {}

    async def connect(self, name: str, script: Path):
        params = StdioServerParameters(command=sys.executable, args=[str(script)])
        read, write = await self.stack.enter_async_context(stdio_client(params))
        session = await self.stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        self.sessions[name] = session
        tools = (await session.list_tools()).tools
        for tool in tools:
            self.tool_to_server[tool.name] = name
        return tools

    async def call(self, tool: str, args: dict) -> str:
        server = self.tool_to_server.get(tool)
        if server is None:
            return f"Unknown tool: {tool}"
        result = await self.sessions[server].call_tool(tool, args)
        return "".join(c.text for c in result.content if getattr(c, "type", "") == "text")

    async def close(self):
        await self.stack.aclose()


def parse_args(parts: list[str]) -> dict:
    """Turn ['a=2', 'text=hello'] into {'a': 2, 'text': 'hello'}."""
    args = {}
    for part in parts:
        key, _, value = part.partition("=")
        try:
            args[key] = json.loads(value)
        except json.JSONDecodeError:
            args[key] = value
    return args


async def main():
    client = MultiServerClient()
    try:
        for name, script in SERVERS.items():
            tools = await client.connect(name, script)
            print(f"[{name}] tools: {', '.join(t.name for t in tools)}")

        print("\n--- Demo calls ---")
        demos = [
            ("add", {"a": 2, "b": 3}),
            ("power", {"base": 2, "exponent": 10}),
            ("word_count", {"text": "MCP makes tools easy to share"}),
            ("reverse_text", {"text": "hello"}),
        ]
        for tool, args in demos:
            print(f"{tool}({args}) -> {await client.call(tool, args)}")

        print("\n--- Interactive mode ---")
        print('Type e.g.  add a=4 b=5   or   to_upper text="hi there"   (quit to exit)')
        while True:
            line = (await asyncio.to_thread(input, "> ")).strip()
            if line in {"quit", "exit"}:
                break
            if not line:
                continue
            tool, *rest = line.split(maxsplit=1)
            import shlex
            tokens = shlex.split(rest[0]) if rest else []
            print(await client.call(tool, parse_args(tokens)))
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
