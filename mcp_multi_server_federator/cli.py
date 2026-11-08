"""CLI for mcp-multi-server-federator."""
import sys
import argparse
from .federator import MCPMultiServerFederator


def main():
    parser = argparse.ArgumentParser(description="MCP Multi-Server Federator CLI")
    parser.add_argument("--demo", action="store_true", help="Run multi-server federator demo")
    args = parser.parse_args()

    if args.demo:
        fed = MCPMultiServerFederator()
        fed.register_server("github", lambda t, a: f"GitHub executed {t}", ["search_code", "create_pr"])
        fed.register_server("postgres", lambda t, a: f"Postgres executed {t}", ["execute_query", "list_tables"])

        print("[+] Unified Federated Tools:")
        for t in fed.list_tools():
            print(f"    - {t}")

        res = fed.call_tool("github.create_pr", {"title": "Update dependencies"})
        print(f"[+] Tool Call Result: {res}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
