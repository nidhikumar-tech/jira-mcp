from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from mcp_client import get_server

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()


async def run_chat():

    print("Starting AI assistant...\n")

    server = get_server()

    async with stdio_client(server) as (read, write):

        session = ClientSession(read, write)

        await session.initialize()

        tools = await load_mcp_tools(session)

        print(f"{len(tools)} MCP tools loaded\n")

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0
        )

        agent = create_react_agent(llm, tools)

        print("Jira / Confluence AI Assistant Ready")
        print("Type 'exit' to quit\n")

        while True:

            query = input("You: ")

            if query.lower() == "exit":
                break

            result = await agent.ainvoke(
                {"messages": [("user", query)]}
            )

            print("\nBot:", result["messages"][-1].content)
            print()