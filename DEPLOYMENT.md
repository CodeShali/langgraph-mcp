# Deployment Guide for LangGraph Cloud

## Prerequisites

✅ LangSmith account: https://smith.langchain.com
✅ GitHub account (for deployment)
✅ MCP server publicly accessible (ngrok URL)

## Files Ready for Deployment

```
langraph/
├── agent_graph.py      # Agent orchestration code
├── langgraph.json      # Deployment configuration
├── requirements.txt    # Dependencies
├── .env               # Environment variables (for reference)
└── mcp_server.py      # Your MCP server (runs separately)
```

## Deployment Steps

### Option 1: Deploy via GitHub (Recommended)

#### Step 1: Create GitHub Repository

```bash
cd /Users/shashankshali/Desktop/langraph

# Initialize git (if not already)
git init

# Create .gitignore to exclude .env
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore

# Add files
git add agent_graph.py langgraph.json requirements.txt mcp_server.py test_mcp_server.py README.md QUICKSTART.md .gitignore

# Commit
git commit -m "Initial commit: LangGraph MCP integration"

# Create repo on GitHub and push
# Go to github.com → New Repository → "langgraph-mcp"
git remote add origin https://github.com/YOUR_USERNAME/langgraph-mcp.git
git branch -M main
git push -u origin main
```

#### Step 2: Connect GitHub to LangSmith

1. Go to https://smith.langchain.com
2. Navigate to **Deployments** → **New Deployment**
3. Choose **GitHub**
4. Authorize LangSmith to access your GitHub
5. Select your repository: `langgraph-mcp`
6. Select branch: `main`
7. LangSmith will detect `langgraph.json` automatically

#### Step 3: Configure Environment Variables

In the deployment settings, add:

```
OPENAI_API_KEY=<your-openai-api-key>

MCP_SERVER_URL=https://c815fb751ca0.ngrok-free.app
```

⚠️ **Important:** Make sure your ngrok is running and the URL is correct!

#### Step 4: Deploy

Click **Deploy** and wait for the build to complete.

You'll get:
- **Deployment URL**: `https://YOUR_DEPLOYMENT.langchain.app`
- **Graph ID**: `agent`

#### Step 5: Create Assistant

After deployment, create an assistant:

**Via LangSmith UI:**
1. Go to your deployment
2. Click **Create Assistant**
3. Name it "MCP Math Assistant"
4. Copy the **Assistant ID**

**Or via API:**
```python
import requests

response = requests.post(
    "https://YOUR_DEPLOYMENT.langchain.app/assistants",
    headers={
        "x-api-key": "YOUR_LANGSMITH_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "graph_id": "agent",
        "name": "MCP Math Assistant"
    }
)

assistant_id = response.json()["assistant_id"]
print(f"Assistant ID: {assistant_id}")
```

### Option 2: Deploy via LangSmith UI (Manual Upload)

#### Step 1: Create a ZIP file

```bash
cd /Users/shashankshali/Desktop/langraph
zip -r deployment.zip agent_graph.py langgraph.json requirements.txt
```

#### Step 2: Upload to LangSmith

1. Go to https://smith.langchain.com
2. Navigate to **Deployments** → **New Deployment**
3. Choose **Upload Files**
4. Upload `deployment.zip`
5. Configure environment variables (same as above)
6. Click **Deploy**

## Testing Your Deployment

### Update langraph_cloud_client.py

Once deployed, update your client to use the real deployment:

```python
# In langraph_cloud_client.py or create a new test file

from langraph_cloud_client import LangGraphCloudClient
import os
from dotenv import load_dotenv

load_dotenv()

# Your deployment details
DEPLOYMENT_URL = "https://YOUR_DEPLOYMENT.langchain.app"  # From LangSmith
ASSISTANT_ID = "asst_YOUR_ID"  # From create assistant step
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

client = LangGraphCloudClient(
    api_key=LANGSMITH_API_KEY,
    base_url=DEPLOYMENT_URL
)

# Create thread
thread = client.create_thread()
print(f"Thread ID: {thread['thread_id']}")

# Run conversation
run = client.create_run(
    thread_id=thread["thread_id"],
    assistant_id=ASSISTANT_ID,
    input_data={
        "messages": [
            {"role": "user", "content": "What is 15 plus 27?"}
        ]
    }
)

# Wait for completion
completed = client.wait_for_run(thread["thread_id"], run["run_id"])

# Get response
state = client.get_thread_state(thread["thread_id"])
messages = state["values"]["messages"]
print(f"Assistant: {messages[-1]['content']}")
```

## Troubleshooting

### Build Failed

**Check:**
- `requirements.txt` has all dependencies
- `langgraph.json` is valid JSON
- `agent_graph.py` has no syntax errors

**View logs:**
- Go to deployment → Logs tab

### Runtime Errors

**"Connection refused" to MCP server:**
- Make sure ngrok is running
- Check `MCP_SERVER_URL` is correct
- Test: `curl https://your-ngrok-url/tools`

**"Module not found":**
- Add missing package to `requirements.txt`
- Redeploy

### Assistant Not Responding

**Check LangSmith traces:**
1. Go to your deployment
2. Click on a run
3. View the trace to see what happened

## Updating Your Deployment

### If you change agent_graph.py:

**GitHub method:**
```bash
git add agent_graph.py
git commit -m "Update agent logic"
git push
# LangSmith auto-deploys on push
```

**Manual method:**
- Create new ZIP
- Upload via LangSmith UI

### If you change MCP server URL:

1. Update environment variable in deployment settings
2. Restart deployment

## Next Steps

After successful deployment:

1. ✅ Test with `langraph_cloud_client.py`
2. ✅ View traces in LangSmith dashboard
3. ✅ Share assistant ID with your team
4. ✅ Build a UI that calls the deployed agent
5. ✅ Monitor usage and costs

## Important Notes

- **MCP Server must stay running** - The deployed agent calls it
- **ngrok URLs expire** - Use a permanent deployment for production
- **Environment variables** - Never commit `.env` to GitHub
- **Costs** - LangGraph Cloud and OpenAI API have usage costs

## Support

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/cloud/
- **LangSmith**: https://smith.langchain.com
- **Discord**: https://discord.gg/langchain
