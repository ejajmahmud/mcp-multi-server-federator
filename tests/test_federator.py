"""Unit tests for mcp-multi-server-federator."""
import unittest
from mcp_multi_server_federator.federator import MCPMultiServerFederator


class TestMCPMultiServerFederator(unittest.TestCase):
    def test_list_and_call(self):
        fed = MCPMultiServerFederator()
        fed.register_server("s1", lambda t, a: f"ok_{t}", ["ping"])
        tools = fed.list_tools()
        self.assertIn("s1.ping", tools)

        res = fed.call_tool("s1.ping", {})
        self.assertEqual(res, "ok_ping")

    def test_missing_prefix_raises(self):
        fed = MCPMultiServerFederator()
        with self.assertRaises(KeyError):
            fed.call_tool("unknown.test", {})
