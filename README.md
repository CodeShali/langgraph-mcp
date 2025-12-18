# LangGraph Cloud MCP Integration

## Overview

This project demonstrates using **LangGraph Cloud Platform APIs** to create an AI assistant that calls your custom **MCP (Model Context Protocol) server**. 

**Key Points:**
- ✅ Uses LangGraph Cloud's **hosted infrastructure** (no code deployment)
- ✅ Your MCP server provides custom tools
- ✅ LangGraph Cloud hosts the LLM and agent runtime
- ✅ Communication via **REST APIs only** (no SDKs)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                         │
│                                                             │
│  langraph_cloud_client.py                                   │
│  (Makes HTTP calls to LangGraph Cloud API)                  │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTPS
                 │ (REST API calls)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              LangGraph Cloud Platform                       │
│              (Hosted by LangChain)                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Your Assistant (hosted)                            │   │
│  │  - GPT-4o-mini LLM                                  │   │
│  │  - Agent orchestration                              │   │
│  │  - Tool calling logic                               │   │
│  └──────────────────┬──────────────────────────────────┘   │
└─────────────────────┼──────────────────────────────────────┘
                      │ HTTPS
                      │ (Calls your MCP tools)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Your MCP Server                                │
│              (Running locally or deployed)                  │
│                                                             │
│  mcp_server.py (Flask)                                      │
│  - http://your-ngrok-url or https://your-server.com         │
│                                                             │
│  Tools:                                                     │
│  - POST /tools/add                                          │
│  - POST /tools/subtract                                     │
│  - POST /tools/multiply                                     │
└─────────────────────────────────────────────────────────────┘
```

## How It Works

1. **You create an assistant** via LangGraph Cloud API
   - Define which tools it can use (your MCP tools)
   - LangGraph Cloud hosts the assistant

2. **User sends a message** via your client
   - Client calls LangGraph Cloud API
   - Creates a "run" in a "thread"

3. **LangGraph Cloud executes**
   - LLM analyzes the message
   - Decides to call your MCP tools
   - Makes HTTP calls to your MCP server
   - Gets results and formulates response

4. **You get the response** via API
   - Poll for run completion
   - Retrieve assistant's response

## Project Structure

```
langraph/
├── mcp_server.py                 # Your MCP server (Flask)
├── langraph_cloud_client.py      # Client for LangGraph Cloud API
├── test_mcp_server.py            # Test your MCP server
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
├── env.example                   # Example env file
└── README.md                     # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Keys

**LangSmith API Key:**
- Go to https://smith.langchain.com
- Sign up/login
- Settings → API Keys → Create new key

**OpenAI API Key:**
- Already in your `.env` file

### 3. Configure Environment

Edit `.env`:
```bash
# Your OpenAI key (already set)
OPENAI_API_KEY=sk-proj-...

# Add your LangSmith key
LANGSMITH_API_KEY=lsv2_pt_your-key-here

# MCP Server URL (must be publicly accessible)
MCP_SERVER_URL=https://your-ngrok-url
```

### 4. Make MCP Server Public

**Option A: Use Cloudflare Tunnel (recommended - free, no signup)**
```bash
# Terminal 1: Start MCP server
python3 mcp_server.py

# Terminal 2: Expose it
brew install cloudflared
cloudflared tunnel --url http://localhost:5000
# Copy the URL to .env as MCP_SERVER_URL
```

**Option B: Use ngrok**
```bash
# Sign up at https://dashboard.ngrok.com/signup
# Get authtoken and configure it
ngrok config add-authtoken YOUR_TOKEN

# Terminal 1: Start MCP server
python3 mcp_server.py

# Terminal 2: Expose it
ngrok http 5000
# Copy the https URL to .env as MCP_SERVER_URL
```

**Option C: Deploy MCP server to cloud**
- Railway.app, Render.com, Fly.io, etc.

### 5. Run the Client

```bash
# Run example
python3 langraph_cloud_client.py

# Or interactive mode
python3 langraph_cloud_client.py interactive
```

## Usage Example

```
======================================================================
LangGraph Cloud API Client - MCP Integration
======================================================================
MCP Server: https://abc123.ngrok.io
======================================================================

1. Fetching tools from MCP server...
   Found 3 tools:
   - add: Add two numbers
   - subtract: Subtract two numbers
   - multiply: Multiply two numbers

2. Creating assistant with MCP tools...
   Created assistant: asst_abc123

3. Creating conversation thread...
   Thread ID: thread_xyz789

4. Running conversation...

   USER: What is 15 plus 27?
   ASSISTANT: The sum of 15 and 27 is 42.

   USER: Now multiply that result by 2
   ASSISTANT: The result is 84.

======================================================================
Demo Complete!
======================================================================
```

## Troubleshooting

### "Could not fetch tools from MCP server"
- Make sure MCP server is running: `python3 mcp_server.py`
- Check `MCP_SERVER_URL` is correct and publicly accessible
- Test: `curl https://your-url/tools`

### "Authentication failed"
- Check `LANGSMITH_API_KEY` is correct
- Get new key from https://smith.langchain.com

### "Connection refused"
- MCP server must be publicly accessible
- Use Cloudflare Tunnel, ngrok, or deploy to cloud
- Cannot use `localhost` for cloud deployments

## Resources

- **LangSmith**: https://smith.langchain.com
- **LangGraph Cloud API**: https://langchain-ai.github.io/langgraph/cloud/reference/api/
