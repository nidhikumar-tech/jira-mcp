# JIRA & Confluence AI Chatbot (MCP + Gemini)

A conversational terminal assistant that bridges **Google Gemini 2.5 Flash** with your Atlassian ecosystem using the **Model Context Protocol (MCP)**. This agent uses **LangGraph** to reason through tasks, searching and updating JIRA issues or Confluence pages in real-time.

---

## Features

* **Natural Language JIRA**: "What bugs are assigned to me?" or "Create a high-priority task for the API fix."
* **Confluence Knowledge Retrieval**: "Find the onboarding docs on Confluence and summarize them."
* **Agentic Reasoning**: Powered by **LangGraph**, the bot autonomously determines which JQL queries or Confluence tools to call based on your intent.
* **Vertex AI Powered**: Enterprise-grade performance and security using Google's Vertex AI backend.

---

## Prerequisites

Before running the chatbot, ensure you have the following installed:

1.  **Python 3.10+**
2.  **uv**: A high-performance Python package manager (required to run the MCP server).
    ```bash
    pip install uv
    ```
3.  **Google Cloud CLI**: Required for Vertex AI authentication.
    ```bash
    # Login and set application default credentials
    gcloud auth login
    gcloud auth application-default login
    ```

---

## Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```
### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a .env file in the root directory and fill in your details:
```bash
# Google Cloud / Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=your-gcp=location

# Atlassian (JIRA & Confluence)
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your-atlassian-api-token

CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-atlassian-api-token

TOOLSETS=all
```
##  Usage
```bash
python chatbot.py
```

## Example Queries
### 1. Fetch all my issues
### 2. Fetch all epics created by me
### 3. Fetch all the stories in the epic &lt;key-id&gt;
