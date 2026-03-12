import asyncio
import os
from dotenv import load_dotenv
from langchain.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent 

load_dotenv()

async def run_chatbot():
    # 1. Added "transport": "stdio" to the config dictionary
    mcp_client = MultiServerMCPClient({
        "atlassian": {
            "transport": "stdio",  # <--- THIS IS THE FIX
            "command": "uvx",
            "args": ["mcp-atlassian"],
            "env": {
                "JIRA_URL": os.getenv("JIRA_URL"),
                "JIRA_USERNAME": os.getenv("JIRA_USERNAME"),
                "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
                "CONFLUENCE_URL": os.getenv("CONFLUENCE_URL"),
                "CONFLUENCE_USERNAME": os.getenv("CONFLUENCE_USERNAME"),
                "CONFLUENCE_API_TOKEN": os.getenv("CONFLUENCE_API_TOKEN"),
                "TOOLSETS": "all"
            }
        }
    })

    # 2. Initialize Gemini 2.5 Flash
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # 3. Fetch tools
    print("Connecting to MCP Servers...")
    tools = await mcp_client.get_tools()

    system_instructions = """
    Your job is to fetch information from JIRA.
    After processing the user's request, and getting an answer from the tool, you should respond with a concise answer to the user.
    If an epic has been asked for, return the epic's name, key, creator, and description. If a list of issues is returned, return the issue keys and summaries, not just the keys.
    Do not ever return the raw tool response to the user, always process it and return a concise answer.
    """
    
    # 4. Create the LangGraph agent
    agent_executor = create_react_agent(llm, tools, prompt=SystemMessage(content=system_instructions))

    print("--- JIRA Chatbot Ready ---")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        try:
            # LangGraph expectation: a list of messages
            response = await agent_executor.ainvoke({"messages": [("human", user_input)]})
            
            # Extract the last message content (the AI's response)
            final_message = response['messages'][-1].content
            print(f"\nGemini: {final_message}")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run_chatbot())