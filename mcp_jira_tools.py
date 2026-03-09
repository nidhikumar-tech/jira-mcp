import os
import json
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

load_dotenv()


async def jira_search_async(jql: str):

    server = StdioServerParameters(
        command="uvx",
        args=["mcp-atlassian"],
        env={
            "JIRA_URL": os.getenv("JIRA_URL"),
            "JIRA_USERNAME": os.getenv("JIRA_USERNAME"),
            "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
            "CONFLUENCE_URL": os.getenv("CONFLUENCE_URL"),
            "CONFLUENCE_USERNAME": os.getenv("CONFLUENCE_USERNAME"),
            "CONFLUENCE_API_TOKEN": os.getenv("CONFLUENCE_API_TOKEN"),
            "TOOLSETS": "all"
        }
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "jira_search",
                {"jql": jql}
            )

            jira_text = result.content[0].text
            jira_data = json.loads(jira_text)

            issues = jira_data["issues"]

            cleaned = []

            for issue in issues:
                cleaned.append({
                    "key": issue["key"],
                    "summary": issue["summary"],
                    "description": issue["description"]
                })

            return cleaned