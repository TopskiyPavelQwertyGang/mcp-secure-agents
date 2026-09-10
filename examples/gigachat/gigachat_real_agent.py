import asyncio
import os

from langchain.agents import create_agent
from langchain_gigachat.chat_models import GigaChat
from langchain_mcp_adapters.client import MultiServerMCPClient


MCP_URL = "http://127.0.0.1:8000/mcp"


async def main():
    print("\n=== GIGACHAT MCP SECURITY AGENT ===\n")

    model = GigaChat(
        credentials=os.environ["GIGACHAT_CREDENTIALS"],
        scope=os.environ["GIGACHAT_SCOPE"],
        model="GigaChat-3-Pro",
        verify_ssl_certs=False,
        streaming=False,
    )

    client = MultiServerMCPClient(
        {
            "vulnerability-agent": {
                "url": MCP_URL,
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()

    print("[MCP] Tools discovered:")

    for tool in tools:
        print(f"  - {tool.name}")

    agent = create_agent(
        model=model,
        tools=tools,
    )

    print("\nAgent ready.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_request = input("USER > ").strip()

        if user_request.lower() in {"exit", "quit"}:
            print("\nSession closed.")
            break

        if not user_request:
            continue

        print("\n[GigaChat] Agent started...\n")

        try:
            response = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_request,
                        }
                    ]
                }
            )

            print("=== AGENT TRACE ===")

            for message in response["messages"]:
                print(f"\n[{type(message).__name__}]")

                content = getattr(message, "content", None)

                if content:
                    print(content)

                tool_calls = getattr(message, "tool_calls", None)

                if tool_calls:
                    print("TOOL CALL:")

                    for call in tool_calls:
                        print(f"  tool: {call['name']}")
                        print(f"  args: {call['args']}")

            print("\n===================")

        except Exception as exc:
            print("\n[ERROR]")
            print(f"{type(exc).__name__}: {exc}")

        print()


if __name__ == "__main__":
    asyncio.run(main())
