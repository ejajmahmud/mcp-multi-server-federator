"""Core MCP Multi-Server Federator implementation."""
from typing import Dict, List, Any, Callable, Optional


class UpstreamServer:
    def __init__(self, prefix: str, handler: Callable[[str, Dict[str, Any]], Any], tools: List[str]):
        self.prefix = prefix
        self.handler = handler
        self.tools = tools


class MCPMultiServerFederator:
    def __init__(self):
        self.servers: Dict[str, UpstreamServer] = {}

    def register_server(self, prefix: str, handler: Callable[[str, Dict[str, Any]], Any], tools: List[str]):
        self.servers[prefix] = UpstreamServer(prefix, handler, tools)

    def list_tools(self) -> List[str]:
        all_tools = []
        for p, s in self.servers.items():
            for t in s.tools:
                all_tools.append(f"{p}.{t}")
        return sorted(all_tools)

    def call_tool(self, federated_name: str, arguments: Dict[str, Any]) -> Any:
        if "." not in federated_name:
            raise ValueError(f"Invalid federated tool name '{federated_name}' (expected prefix.tool)")

        prefix, tool = federated_name.split(".", 1)
        if prefix not in self.servers:
            raise KeyError(f"No upstream server registered for prefix '{prefix}'")

        server = self.servers[prefix]
        if tool not in server.tools:
            raise KeyError(f"Tool '{tool}' not found on upstream server '{prefix}'")

        return server.handler(tool, arguments)
