"""
Simple Web API wrapper around your working LangGraph client
Exposes your local agent as a web API that can be accessed remotely
"""

from flask import Flask, request, jsonify
import uuid
import sys
import os
import subprocess
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# In-memory storage
threads = {}
assistants = {}
runs = {}

# ============================================================================
# Helper function to run the local agent
# ============================================================================

def run_agent_query(query):
    """
    Run a query through a subprocess to avoid Python 3.9 compatibility issues
    Returns the agent's response
    """
    try:
        import subprocess
        import json
        
        # Run the query through a subprocess
        result = subprocess.run(
            ["python3", "query_agent.py", query],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            response_data = json.loads(result.stdout)
            return response_data.get("response", "No response")
        else:
            return f"Error running query: {result.stderr}"
            
    except Exception as e:
        return f"Error running agent: {str(e)}"

# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy", 
        "server": "Simple Local LangGraph API",
        "mcp_server": os.getenv("MCP_SERVER_URL", "http://localhost:5000")
    })

@app.route('/assistants', methods=['POST'])
def create_assistant():
    """Create an assistant (just returns a mock ID)"""
    data = request.json or {}
    assistant_id = f"asst_{uuid.uuid4().hex[:8]}"
    
    assistant = {
        "assistant_id": assistant_id,
        "name": data.get("name", "Local Math Assistant"),
        "graph_id": "agent",
        "created_at": "2024-01-01T00:00:00Z"
    }
    
    assistants[assistant_id] = assistant
    return jsonify(assistant)

@app.route('/assistants/<assistant_id>', methods=['GET'])
def get_assistant(assistant_id):
    """Get assistant details"""
    if assistant_id not in assistants:
        return jsonify({"error": "Assistant not found"}), 404
    return jsonify(assistants[assistant_id])

@app.route('/threads', methods=['POST'])
def create_thread():
    """Create a conversation thread"""
    thread_id = f"thread_{uuid.uuid4().hex[:8]}"
    
    thread = {
        "thread_id": thread_id,
        "metadata": request.json.get("metadata", {}) if request.json else {},
        "created_at": "2024-01-01T00:00:00Z"
    }
    
    threads[thread_id] = {
        **thread,
        "messages": []
    }
    
    return jsonify(thread)

@app.route('/threads/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    """Get thread info"""
    if thread_id not in threads:
        return jsonify({"error": "Thread not found"}), 404
    
    thread = threads[thread_id].copy()
    del thread["messages"]
    return jsonify(thread)

@app.route('/threads/<thread_id>/state', methods=['GET'])
def get_thread_state(thread_id):
    """Get thread state with messages"""
    if thread_id not in threads:
        return jsonify({"error": "Thread not found"}), 404
    
    return jsonify({
        "values": {
            "messages": threads[thread_id]["messages"]
        }
    })

@app.route('/threads/<thread_id>/runs', methods=['POST'])
def create_run(thread_id):
    """Create and execute a run"""
    if thread_id not in threads:
        return jsonify({"error": "Thread not found"}), 404
    
    data = request.json
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    
    # Get user message
    input_messages = data.get("input", {}).get("messages", [])
    user_message = None
    
    for msg in input_messages:
        if msg["role"] == "user":
            user_message = msg["content"]
            break
    
    if not user_message:
        return jsonify({"error": "No user message found"}), 400
    
    # Add user message to thread
    threads[thread_id]["messages"].append({
        "role": "user",
        "content": user_message,
        "type": "human"
    })
    
    # Run the agent using the real agent logic
    try:
        agent_response = run_agent_query(user_message)
        
        # Add agent response to thread
        threads[thread_id]["messages"].append({
            "role": "assistant", 
            "content": agent_response,
            "type": "ai"
        })
        
        run = {
            "run_id": run_id,
            "thread_id": thread_id,
            "assistant_id": data.get("assistant_id"),
            "status": "success",
            "created_at": "2024-01-01T00:00:00Z",
            "completed_at": "2024-01-01T00:00:01Z"
        }
        
    except Exception as e:
        run = {
            "run_id": run_id,
            "thread_id": thread_id,
            "assistant_id": data.get("assistant_id"),
            "status": "error",
            "error": str(e),
            "created_at": "2024-01-01T00:00:00Z",
            "completed_at": "2024-01-01T00:00:01Z"
        }
    
    runs[run_id] = run
    return jsonify(run)

@app.route('/threads/<thread_id>/runs/<run_id>', methods=['GET'])
def get_run(thread_id, run_id):
    """Get run details"""
    if run_id not in runs:
        return jsonify({"error": "Run not found"}), 404
    return jsonify(runs[run_id])

# ============================================================================
# Test endpoint to verify MCP server connection
# ============================================================================

@app.route('/test-mcp', methods=['GET'])
def test_mcp():
    """Test connection to MCP server"""
    import requests
    
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:5000")
    
    try:
        response = requests.get(f"{mcp_url}/health", timeout=5)
        return jsonify({
            "mcp_server": mcp_url,
            "status": "connected",
            "response": response.json()
        })
    except Exception as e:
        return jsonify({
            "mcp_server": mcp_url,
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    print("=" * 60)
    print("Simple Local LangGraph API Server")
    print("=" * 60)
    print(f"MCP Server: {os.getenv('MCP_SERVER_URL', 'http://localhost:5000')}")
    print("Starting server on http://localhost:8000")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /health           - Server health")
    print("  GET  /test-mcp         - Test MCP connection")
    print("  POST /assistants       - Create assistant")
    print("  POST /threads          - Create thread")
    print("  POST /threads/{id}/runs - Run conversation")
    print("=" * 60)
    print("\nTo expose publicly:")
    print("  ngrok http 8000")
    print("  or")
    print("  cloudflared tunnel --url http://localhost:8000")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=8000, debug=True)
