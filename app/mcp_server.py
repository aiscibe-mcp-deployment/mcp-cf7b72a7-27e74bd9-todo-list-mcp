import json
import logging
import os
from typing import Any
from mcp.server.fastmcp import FastMCP
import httpx

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

PROJECT_NAME = "Todo List MCP"
API_CONNECTIONS = {
    "default": {"base_url": "https://jsonplaceholder.typicode.com", "auth_type": "none", "auth_config": {}},
}

client = httpx.AsyncClient(timeout=30.0)


def _get_auth_headers(conn_name: str) -> dict:
    conn = API_CONNECTIONS.get(conn_name, {})
    auth_type = conn.get("auth_type")
    auth_config = conn.get("auth_config", {})
    headers = {}

    if auth_type == "api_key":
        headers[auth_config.get("key_name", "X-API-Key")] = auth_config.get("api_key", "")

    elif auth_type == "bearer":
        headers["Authorization"] = f"Bearer {auth_config.get('token', '')}"

    return headers


async def call_api(method: str, endpoint: str, **kwargs) -> str:
    conn_name = "default"
    url = f"{API_CONNECTIONS[conn_name]['base_url']}{endpoint}"
    headers = _get_auth_headers(conn_name)

    try:
        if method == "GET":
            response = await client.get(url, params=kwargs, headers=headers)
        elif method == "POST":
            response = await client.post(url, json=kwargs, headers=headers)
        else:
            return json.dumps({"error": f"Unsupported method: {method}"})

        response.raise_for_status()
        return response.text

    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return json.dumps({"error": str(e)})


mcp = FastMCP(PROJECT_NAME)


@mcp.tool()
async def get_todos(limit: int = 10) -> str:
    result = await call_api("GET", "/todos")
    todos = json.loads(result)
    return json.dumps(todos[:limit])


@mcp.tool()
async def get_todo(todo_id: int) -> str:
    return await call_api("GET", f"/todos/{todo_id}")


@mcp.tool()
async def create_todo(title: str, completed: bool = False) -> str:
    return await call_api("POST", "/todos", title=title, completed=completed)


def main():
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    logger.info(f"Starting {PROJECT_NAME} MCP server on {host}:{port}...")
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
