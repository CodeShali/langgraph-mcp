# Setup Guide

## Prerequisites

- **Python 3.9+** (Python 3.11+ recommended for full features)
- **macOS/Linux** (Windows with WSL should work)
- **OpenAI API Key** (required)
- **Internet connection** (for public access)

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/CodeShali/langgraph-mcp.git
cd langgraph-mcp
./scripts/setup.sh
```

### 2. Configure Environment

Edit `.env` file:
```bash
# Required
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Optional
LANGSMITH_API_KEY=your-langsmith-key-here
```

### 3. Start Services

```bash
./scripts/start.sh
```

This will:
- Start MCP server on `http://localhost:5000`
- Start API server on `http://localhost:8000`
- Expose API publicly via Cloudflare Tunnel
- Display the public URL

### 4. Test Deployment

```bash
python3 scripts/test.py
```

## Manual Setup

If you prefer manual setup:

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Start MCP Server

```bash
python3 mcp_server.py
```

### 3. Start API Server

```bash
python3 simple_web_api.py
```

### 4. Expose Publicly (Optional)

```bash
# Install cloudflared
brew install cloudflared  # macOS
# or download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

# Expose API server
cloudflared tunnel --url http://localhost:8000
```

## Verification

### Local Endpoints

- **MCP Server Health**: `curl http://localhost:5000/health`
- **API Server Health**: `curl http://localhost:8000/health`
- **MCP Tools**: `curl http://localhost:5000/tools`

### Test API

```bash
# Create assistant
curl -X POST http://localhost:8000/assistants \
  -H "Content-Type: application/json" \
  -d '{"name": "Math Assistant"}'

# Create thread
curl -X POST http://localhost:8000/threads \
  -H "Content-Type: application/json" \
  -d '{}'

# Run query (replace thread_id and assistant_id)
curl -X POST http://localhost:8000/threads/THREAD_ID/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "ASSISTANT_ID",
    "input": {
      "messages": [{"role": "user", "content": "What is 5 + 3?"}]
    }
  }'
```

## Troubleshooting

### "Module not found" errors

```bash
pip3 install -r requirements.txt
```

### "Connection refused" errors

- Make sure MCP server is running: `python3 mcp_server.py`
- Check if ports 5000 and 8000 are available

### "OpenAI API key" errors

- Verify your API key in `.env` file
- Test: `curl -H "Authorization: Bearer YOUR_KEY" https://api.openai.com/v1/models`

### Cloudflared not found

```bash
# macOS
brew install cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

## Architecture

```
Internet → Cloudflare Tunnel → API Server → Query Agent → MCP Server → Math Tools
```

- **MCP Server**: Provides math tools (add, subtract, multiply)
- **API Server**: LangGraph-compatible REST API
- **Query Agent**: Processes queries and calls appropriate tools
- **Cloudflare Tunnel**: Exposes local API publicly

## Next Steps

- See [API.md](API.md) for API documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [DEVELOPMENT.md](DEVELOPMENT.md) for extending the project
