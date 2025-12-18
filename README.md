# LangGraph MCP Local Deployment

## Overview

A **local AI agent deployment** with **cloud accessibility** that integrates custom MCP (Model Context Protocol) tools. This provides LangGraph Cloud-compatible APIs without cloud billing.

**Key Features:**
- 🏠 **Local deployment** - runs on your machine
- 🌐 **Cloud accessible** - public HTTPS endpoint via Cloudflare Tunnel
- 🔧 **Custom MCP tools** - math operations (add, subtract, multiply)
- 🚀 **LangGraph-compatible API** - same endpoints as LangGraph Cloud
- 💰 **Cost-effective** - only OpenAI API usage, no cloud hosting fees

## Quick Start

### 1. Setup

```bash
git clone https://github.com/CodeShali/langgraph-mcp.git
cd langgraph-mcp
./scripts/setup.sh
```

### 2. Configure

Edit `.env` file:
```bash
OPENAI_API_KEY=sk-proj-your-openai-key-here
```

### 3. Start

```bash
./scripts/start.sh
```

### 4. Test

```bash
python3 scripts/test.py
```

## Architecture

```
Internet → Cloudflare Tunnel → API Server → Query Agent → MCP Server → Math Tools
```

**Components:**
- **MCP Server** (`mcp_server.py`): Provides math tools via HTTP
- **API Server** (`simple_web_api.py`): LangGraph-compatible REST API
- **Query Agent** (`query_agent.py`): Processes queries and calls tools
- **Cloudflare Tunnel**: Exposes local API publicly

## Project Structure

```
langgraph-mcp/
├── mcp_server.py           # MCP server with math tools
├── simple_web_api.py       # Main API server
├── query_agent.py          # Query processing logic
├── test_mcp_server.py      # MCP server tests
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── env.example             # Environment template
├── scripts/
│   ├── setup.sh           # Setup script
│   ├── start.sh           # Start all services
│   └── test.py            # Test deployment
└── docs/
    ├── SETUP.md           # Detailed setup guide
    └── API.md             # API documentation
```

## API Endpoints

### Core Endpoints
- `GET /health` - Server health check
- `POST /assistants` - Create assistant
- `POST /threads` - Create conversation thread
- `POST /threads/{id}/runs` - Execute agent
- `GET /threads/{id}/state` - Get conversation state

### Example Usage

```python
import requests

base_url = "http://localhost:8000"  # or your public URL

# Create assistant
assistant = requests.post(f"{base_url}/assistants", 
                         json={"name": "Math Helper"}).json()

# Create thread
thread = requests.post(f"{base_url}/threads").json()

# Send query
run = requests.post(f"{base_url}/threads/{thread['thread_id']}/runs",
                   json={
                       "assistant_id": assistant["assistant_id"],
                       "input": {
                           "messages": [{"role": "user", "content": "What is 15 + 27?"}]
                       }
                   })

# Get response
state = requests.get(f"{base_url}/threads/{thread['thread_id']}/state").json()
print(state["values"]["messages"][-1]["content"])
```

## MCP Tools

The agent can use these math tools:

- **add_numbers(a, b)** - Add two numbers
- **subtract_numbers(a, b)** - Subtract b from a
- **multiply_numbers(a, b)** - Multiply two numbers

## Deployment Options

### Local Development
```bash
./scripts/start.sh
```
Access at: `http://localhost:8000`

### Public Access
The start script automatically exposes your API via Cloudflare Tunnel.
You'll get a public URL like: `https://xxx-xxx-xxx.trycloudflare.com`

### Production Deployment
For production, deploy the MCP server to a cloud service and update the `MCP_SERVER_URL` in your environment.

## Requirements

- **Python 3.9+** (Python 3.11+ recommended)
- **OpenAI API Key** (required)
- **Internet connection** (for public access)
- **macOS/Linux** (Windows with WSL)

## Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed setup instructions
- **[API Documentation](docs/API.md)** - Complete API reference

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip3 install -r requirements.txt
```

**"Connection refused" errors:**
- Ensure MCP server is running: `python3 mcp_server.py`
- Check ports 5000 and 8000 are available

**"OpenAI API key" errors:**
- Verify your API key in `.env` file
- Test: `curl -H "Authorization: Bearer YOUR_KEY" https://api.openai.com/v1/models`

### Getting Help

1. Check the [Setup Guide](docs/SETUP.md)
2. Run the test script: `python3 scripts/test.py`
3. Check server logs in the terminal

## Benefits

✅ **No cloud billing** - runs locally  
✅ **Cloud accessibility** - public HTTPS endpoint  
✅ **LangGraph compatibility** - same API as LangGraph Cloud  
✅ **Custom tools** - your own MCP server  
✅ **Easy deployment** - one command setup  
✅ **Cost control** - only OpenAI API usage  

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
