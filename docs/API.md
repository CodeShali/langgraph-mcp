# API Documentation

## Overview

This API provides LangGraph Cloud-compatible endpoints for interacting with a local AI agent that uses custom MCP (Model Context Protocol) tools.

**Base URL**: `http://localhost:8000` (local) or your Cloudflare tunnel URL

## Authentication

No authentication required for local deployment.

## Endpoints

### Health Check

**GET** `/health`

Check server health and configuration.

**Response:**
```json
{
  "status": "healthy",
  "server": "Simple Local LangGraph API",
  "mcp_server": "http://localhost:5000"
}
```

### Test MCP Connection

**GET** `/test-mcp`

Test connection to the MCP server.

**Response:**
```json
{
  "mcp_server": "http://localhost:5000",
  "status": "connected",
  "response": {
    "service": "MCP Math Server",
    "status": "healthy"
  }
}
```

### Create Assistant

**POST** `/assistants`

Create a new assistant instance.

**Request Body:**
```json
{
  "name": "Math Assistant",
  "graph_id": "agent"
}
```

**Response:**
```json
{
  "assistant_id": "asst_12345678",
  "name": "Math Assistant",
  "graph_id": "agent",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Get Assistant

**GET** `/assistants/{assistant_id}`

Get assistant details.

**Response:**
```json
{
  "assistant_id": "asst_12345678",
  "name": "Math Assistant",
  "graph_id": "agent",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Create Thread

**POST** `/threads`

Create a new conversation thread.

**Request Body (optional):**
```json
{
  "metadata": {
    "user": "demo",
    "session": "test"
  }
}
```

**Response:**
```json
{
  "thread_id": "thread_87654321",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Get Thread

**GET** `/threads/{thread_id}`

Get thread information (without messages).

**Response:**
```json
{
  "thread_id": "thread_87654321",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Get Thread State

**GET** `/threads/{thread_id}/state`

Get thread state including all messages.

**Response:**
```json
{
  "values": {
    "messages": [
      {
        "role": "user",
        "content": "What is 5 + 3?",
        "type": "human"
      },
      {
        "role": "assistant",
        "content": "I would use the add tool to calculate this math problem.",
        "type": "ai"
      }
    ]
  }
}
```

### Create Run

**POST** `/threads/{thread_id}/runs`

Execute the assistant with a new message.

**Request Body:**
```json
{
  "assistant_id": "asst_12345678",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "What is 15 plus 27?"
      }
    ]
  }
}
```

**Response:**
```json
{
  "run_id": "run_11111111",
  "thread_id": "thread_87654321",
  "assistant_id": "asst_12345678",
  "status": "success",
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:00:01Z"
}
```

### Get Run

**GET** `/threads/{thread_id}/runs/{run_id}`

Get run details and status.

**Response:**
```json
{
  "run_id": "run_11111111",
  "thread_id": "thread_87654321",
  "assistant_id": "asst_12345678",
  "status": "success",
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:00:01Z"
}
```

## Usage Examples

### Basic Conversation

```python
import requests

base_url = "http://localhost:8000"

# 1. Create assistant
assistant = requests.post(f"{base_url}/assistants", 
                         json={"name": "Math Helper"}).json()
assistant_id = assistant["assistant_id"]

# 2. Create thread
thread = requests.post(f"{base_url}/threads").json()
thread_id = thread["thread_id"]

# 3. Send message
run = requests.post(f"{base_url}/threads/{thread_id}/runs",
                   json={
                       "assistant_id": assistant_id,
                       "input": {
                           "messages": [{"role": "user", "content": "What is 10 + 5?"}]
                       }
                   }).json()

# 4. Get response
state = requests.get(f"{base_url}/threads/{thread_id}/state").json()
messages = state["values"]["messages"]
print(f"Response: {messages[-1]['content']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const baseURL = 'http://localhost:8000';

async function chatWithAssistant(query) {
    // Create assistant
    const assistant = await axios.post(`${baseURL}/assistants`, {
        name: 'Math Helper'
    });
    const assistantId = assistant.data.assistant_id;
    
    // Create thread
    const thread = await axios.post(`${baseURL}/threads`);
    const threadId = thread.data.thread_id;
    
    // Send message
    await axios.post(`${baseURL}/threads/${threadId}/runs`, {
        assistant_id: assistantId,
        input: {
            messages: [{ role: 'user', content: query }]
        }
    });
    
    // Get response
    const state = await axios.get(`${baseURL}/threads/${threadId}/state`);
    const messages = state.data.values.messages;
    return messages[messages.length - 1].content;
}

// Usage
chatWithAssistant("What is 20 * 3?").then(console.log);
```

### cURL Examples

```bash
# Create assistant
ASSISTANT_ID=$(curl -s -X POST http://localhost:8000/assistants \
  -H "Content-Type: application/json" \
  -d '{"name": "Math Helper"}' | jq -r .assistant_id)

# Create thread
THREAD_ID=$(curl -s -X POST http://localhost:8000/threads \
  -H "Content-Type: application/json" \
  -d '{}' | jq -r .thread_id)

# Send message
curl -X POST http://localhost:8000/threads/$THREAD_ID/runs \
  -H "Content-Type: application/json" \
  -d "{
    \"assistant_id\": \"$ASSISTANT_ID\",
    \"input\": {
      \"messages\": [{\"role\": \"user\", \"content\": \"What is 7 + 8?\"}]
    }
  }"

# Get response
curl http://localhost:8000/threads/$THREAD_ID/state | jq '.values.messages[-1].content'
```

## Error Handling

### Error Response Format

```json
{
  "error": "Error message description"
}
```

### Common HTTP Status Codes

- **200**: Success
- **400**: Bad Request (missing required fields)
- **404**: Not Found (thread/assistant/run not found)
- **500**: Internal Server Error

### Common Errors

- **"No user message found"**: The input.messages array is empty or missing
- **"Thread not found"**: Invalid thread_id
- **"Assistant not found"**: Invalid assistant_id
- **"Run not found"**: Invalid run_id

## Rate Limiting

No rate limiting is implemented in the local deployment. For production use, consider adding rate limiting middleware.

## MCP Tools

The assistant can use these math tools via the MCP server:

- **add_numbers(a, b)**: Add two numbers
- **subtract_numbers(a, b)**: Subtract b from a  
- **multiply_numbers(a, b)**: Multiply two numbers

The assistant will automatically detect when to use these tools based on the user's query.
