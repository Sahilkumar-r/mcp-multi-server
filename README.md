# mcp-multi-server-demo

A minimal [Model Context Protocol (MCP)](https://modelcontextprotocol.io) example: **two servers** and **one client** that talks to both over stdio.

## Project structure

```
mcp-multi-server-demo/
├── servers/
│   ├── math_server.py   # tools: add, multiply, power
│   └── text_server.py   # tools: word_count, reverse_text, to_upper
├── client.py            # connects to both servers, lists and calls tools
├── requirements.txt
└── README.md
```

## How it works

- Each server uses `FastMCP` and exposes plain Python functions as MCP tools.
- The client launches each server as a subprocess (stdio transport), initializes a session with it, and lists its tools.
- The client keeps a map of `tool name -> server`, so a call is routed to the right server automatically.

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python client.py
```

You will see the tools discovered on each server, a few demo calls, and then an interactive prompt:

```
> add a=4 b=5
9.0
> to_upper text="hello mcp"
HELLO MCP
> quit
```

You can also inspect a server on its own with the MCP Inspector:

```bash
mcp dev servers/math_server.py
```

## Extending

- Add a new function with `@mcp.tool()` in either server and restart the client.
- Add another server file and register it in the `SERVERS` dict in `client.py`.
- Connect the client to an LLM (e.g. the Claude API) and pass the discovered tools so the model can call them.

## License

MIT
