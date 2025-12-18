# Quick Start Guide

## Prerequisites
- Python 3.10+
- LangSmith account (free): https://smith.langchain.com

## Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get LangSmith API Key
1. Go to https://smith.langchain.com
2. Sign up/login
3. Settings → API Keys → Create new key
4. Copy the key

### 3. Update .env File
```bash
# Edit .env and add:
LANGSMITH_API_KEY=lsv2_pt_your-key-here
```

### 4. Start MCP Server
```bash
# Terminal 1
python3 mcp_server.py
```

### 5. Expose MCP Server (choose one)

**Option A: Cloudflare Tunnel (recommended)**
```bash
# Terminal 2
brew install cloudflared
cloudflared tunnel --url http://localhost:5000

# Copy the https URL (e.g., https://abc-123.trycloudflare.com)
# Update .env: MCP_SERVER_URL=https://abc-123.trycloudflare.com
```

**Option B: ngrok**
```bash
# Sign up at https://dashboard.ngrok.com
# Get authtoken and configure
ngrok config add-authtoken YOUR_TOKEN

# Terminal 2
ngrok http 5000

# Copy the https URL
# Update .env: MCP_SERVER_URL=https://abc123.ngrok.io
```

### 6. Run the Client
```bash
# Terminal 3 (or after updating .env)
python3 langraph_cloud_client.py

# Or for interactive mode:
python3 langraph_cloud_client.py interactive
```

## Expected Output

```
======================================================================
LangGraph Cloud API Client - MCP Integration
======================================================================
MCP Server: https://your-url.com
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
```

## Troubleshooting

**"Could not fetch tools"**
- Check MCP server is running
- Check MCP_SERVER_URL is publicly accessible
- Test: `curl https://your-url/tools`

**"Authentication failed"**
- Check LANGSMITH_API_KEY in .env
- Make sure you copied the full key

**"Connection refused"**
- MCP server must be public (not localhost)
- Use Cloudflare Tunnel or ngrok

## Next Steps

- Try interactive mode: `python3 langraph_cloud_client.py interactive`
- Add more tools to `mcp_server.py`
- Deploy MCP server to cloud for production
- View traces in LangSmith dashboard
