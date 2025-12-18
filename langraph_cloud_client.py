"""
LangGraph Cloud API Client
This client uses LangGraph Cloud's hosted infrastructure via REST APIs.
No code deployment needed - LangGraph Cloud hosts the agent runtime.
"""

import requests
import json
import time
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LangGraphCloudClient:
    """
    Client for LangGraph Cloud Platform API.
    Creates assistants that run on LangGraph's infrastructure and call your MCP server.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.langchain.com"):
        """
        Initialize the LangGraph Cloud client.
        
        Args:
            api_key: Your LangSmith API key
            base_url: LangGraph Cloud API base URL
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    # ============================================================================
    # Assistant Management
    # ============================================================================
    
    def create_assistant(
        self,
        name: str,
        graph_id: str,
        config: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create an assistant (agent configuration).
        
        Args:
            name: Name for the assistant
            graph_id: Graph/agent type identifier
            config: Configuration for the assistant
            metadata: Optional metadata
        
        Returns:
            Assistant object with assistant_id
        """
        url = f"{self.base_url}/assistants"
        
        payload = {
            "name": name,
            "graph_id": graph_id
        }
        
        if config:
            payload["config"] = config
        if metadata:
            payload["metadata"] = metadata
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def list_assistants(self) -> List[Dict[str, Any]]:
        """
        List all assistants.
        
        Returns:
            List of assistant objects
        """
        url = f"{self.base_url}/assistants"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """
        Get assistant details.
        
        Args:
            assistant_id: ID of the assistant
        
        Returns:
            Assistant object
        """
        url = f"{self.base_url}/assistants/{assistant_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def update_assistant(
        self,
        assistant_id: str,
        name: Optional[str] = None,
        config: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Update an assistant.
        
        Args:
            assistant_id: ID of the assistant
            name: New name
            config: New configuration
            metadata: New metadata
        
        Returns:
            Updated assistant object
        """
        url = f"{self.base_url}/assistants/{assistant_id}"
        
        payload = {}
        if name:
            payload["name"] = name
        if config:
            payload["config"] = config
        if metadata:
            payload["metadata"] = metadata
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def delete_assistant(self, assistant_id: str) -> None:
        """
        Delete an assistant.
        
        Args:
            assistant_id: ID of the assistant to delete
        """
        url = f"{self.base_url}/assistants/{assistant_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
    
    # ============================================================================
    # Thread Management
    # ============================================================================
    
    def create_thread(self, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a conversation thread.
        
        Args:
            metadata: Optional metadata for the thread
        
        Returns:
            Thread object with thread_id
        """
        url = f"{self.base_url}/threads"
        
        payload = {}
        if metadata:
            payload["metadata"] = metadata
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Get thread details.
        
        Args:
            thread_id: ID of the thread
        
        Returns:
            Thread object
        """
        url = f"{self.base_url}/threads/{thread_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def delete_thread(self, thread_id: str) -> None:
        """
        Delete a thread.
        
        Args:
            thread_id: ID of the thread to delete
        """
        url = f"{self.base_url}/threads/{thread_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
    
    # ============================================================================
    # Run Management (Execute Agent)
    # ============================================================================
    
    def create_run(
        self,
        thread_id: str,
        assistant_id: str,
        input_data: Dict[str, Any],
        config: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Create a run (execute the assistant/agent).
        
        Args:
            thread_id: ID of the thread
            assistant_id: ID of the assistant
            input_data: Input data (e.g., {"messages": [...]})
            config: Optional runtime configuration
            metadata: Optional metadata
            stream: Whether to stream the response
        
        Returns:
            Run object with run_id
        """
        url = f"{self.base_url}/threads/{thread_id}/runs"
        
        payload = {
            "assistant_id": assistant_id,
            "input": input_data
        }
        
        if config:
            payload["config"] = config
        if metadata:
            payload["metadata"] = metadata
        if stream:
            payload["stream_mode"] = "values"
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_run(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        """
        Get run status and results.
        
        Args:
            thread_id: ID of the thread
            run_id: ID of the run
        
        Returns:
            Run object with status and results
        """
        url = f"{self.base_url}/threads/{thread_id}/runs/{run_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def wait_for_run(
        self,
        thread_id: str,
        run_id: str,
        timeout: int = 60,
        poll_interval: float = 1.0
    ) -> Dict[str, Any]:
        """
        Wait for a run to complete.
        
        Args:
            thread_id: ID of the thread
            run_id: ID of the run
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
        
        Returns:
            Completed run object
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            run = self.get_run(thread_id, run_id)
            status = run.get("status")
            
            if status in ["success", "error", "timeout", "interrupted"]:
                return run
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Run {run_id} did not complete within {timeout} seconds")
    
    def get_thread_state(self, thread_id: str) -> Dict[str, Any]:
        """
        Get the current state of a thread.
        
        Args:
            thread_id: ID of the thread
        
        Returns:
            Thread state including messages
        """
        url = f"{self.base_url}/threads/{thread_id}/state"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def stream_run(
        self,
        thread_id: str,
        assistant_id: str,
        input_data: Dict[str, Any]
    ):
        """
        Stream a run (execute agent with streaming).
        
        Args:
            thread_id: ID of the thread
            assistant_id: ID of the assistant
            input_data: Input data
        
        Yields:
            Streamed events
        """
        url = f"{self.base_url}/threads/{thread_id}/runs/stream"
        
        payload = {
            "assistant_id": assistant_id,
            "input": input_data,
            "stream_mode": "values"
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = line_str[6:]
                    if data.strip():
                        yield json.loads(data)


# ============================================================================
# MCP Tool Registration Helper
# ============================================================================

def get_mcp_tools_schema(mcp_server_url: str) -> List[Dict[str, Any]]:
    """
    Fetch tool schemas from MCP server and convert to LangGraph format.
    
    Args:
        mcp_server_url: URL of your MCP server
    
    Returns:
        List of tool schemas in LangGraph format
    """
    response = requests.get(f"{mcp_server_url}/tools")
    response.raise_for_status()
    response_data = response.json()
    
    # Handle both {"tools": [...]} and [...] formats
    mcp_tools = response_data.get("tools", response_data) if isinstance(response_data, dict) else response_data
    
    # Convert MCP tool format to LangGraph tool format
    langraph_tools = []
    
    for tool in mcp_tools:
        langraph_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
        
        # Add parameters (handle both inputSchema and input_schema)
        input_schema = tool.get("input_schema") or tool.get("inputSchema", {})
        for param_name, param_schema in input_schema.get("properties", {}).items():
            langraph_tool["function"]["parameters"]["properties"][param_name] = param_schema
            
            # Add to required if needed
            if param_name in input_schema.get("required", []):
                langraph_tool["function"]["parameters"]["required"].append(param_name)
        
        langraph_tools.append(langraph_tool)
    
    return langraph_tools


# ============================================================================
# Example Usage
# ============================================================================

def main():
    """
    Example: Create assistant with MCP tools and run conversations.
    """
    # Configuration
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:5000")
    
    if not LANGSMITH_API_KEY:
        print("ERROR: LANGSMITH_API_KEY not set in environment")
        print("Get your key from: https://smith.langchain.com")
        return
    
    print("=" * 70)
    print("LangGraph Cloud API Client - MCP Integration")
    print("=" * 70)
    print(f"MCP Server: {MCP_SERVER_URL}")
    print("=" * 70)
    
    # Initialize client
    client = LangGraphCloudClient(api_key=LANGSMITH_API_KEY)
    
    # Step 1: Get MCP tools
    print("\n1. Fetching tools from MCP server...")
    try:
        tools = get_mcp_tools_schema(MCP_SERVER_URL)
        print(f"   Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool['function']['name']}: {tool['function']['description']}")
    except Exception as e:
        print(f"   ERROR: Could not fetch tools from MCP server: {e}")
        print(f"   Make sure MCP server is running at {MCP_SERVER_URL}")
        return
    
    # Step 2: Create assistant with MCP tools
    print("\n2. Creating assistant with MCP tools...")
    try:
        assistant = client.create_assistant(
            name="MCP Math Assistant",
            graph_id="agent",  # Standard agent graph
            config={
                "configurable": {
                    "model": "gpt-4o-mini",
                    "tools": tools,
                    "mcp_server_url": MCP_SERVER_URL
                }
            },
            metadata={
                "description": "Math assistant using custom MCP server",
                "mcp_server": MCP_SERVER_URL
            }
        )
        assistant_id = assistant["assistant_id"]
        print(f"   Created assistant: {assistant_id}")
    except Exception as e:
        print(f"   ERROR: Could not create assistant: {e}")
        print(f"   Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return
    
    # Step 3: Create thread
    print("\n3. Creating conversation thread...")
    thread = client.create_thread(metadata={"user": "demo"})
    thread_id = thread["thread_id"]
    print(f"   Thread ID: {thread_id}")
    
    # Step 4: Run conversation
    print("\n4. Running conversation...")
    queries = [
        "What is 15 plus 27?",
        "Now multiply that result by 2"
    ]
    
    for query in queries:
        print(f"\n   USER: {query}")
        
        # Create run
        run = client.create_run(
            thread_id=thread_id,
            assistant_id=assistant_id,
            input_data={
                "messages": [
                    {"role": "user", "content": query}
                ]
            }
        )
        
        # Wait for completion
        print("   Thinking...", end="", flush=True)
        completed_run = client.wait_for_run(thread_id, run["run_id"])
        print("\r" + " " * 20, end="\r")
        
        # Get response
        state = client.get_thread_state(thread_id)
        last_message = state.get("values", {}).get("messages", [])[-1]
        print(f"   ASSISTANT: {last_message.get('content', '')}")
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print(f"\nAssistant ID: {assistant_id}")
    print(f"Thread ID: {thread_id}")
    print("\nYou can continue this conversation by creating more runs with the same thread_id")


def interactive():
    """
    Interactive mode for chatting with the assistant.
    """
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:5000")
    
    if not LANGSMITH_API_KEY:
        print("ERROR: LANGSMITH_API_KEY not set")
        return
    
    client = LangGraphCloudClient(api_key=LANGSMITH_API_KEY)
    
    # Get or create assistant
    print("Fetching tools and creating assistant...")
    tools = get_mcp_tools_schema(MCP_SERVER_URL)
    
    assistant = client.create_assistant(
        name="MCP Math Assistant",
        graph_id="agent",
        config={
            "configurable": {
                "model": "gpt-4o-mini",
                "tools": tools,
                "mcp_server_url": MCP_SERVER_URL
            }
        }
    )
    assistant_id = assistant["assistant_id"]
    
    # Create thread
    thread = client.create_thread()
    thread_id = thread["thread_id"]
    
    print("\n" + "=" * 70)
    print("Interactive Mode - Type 'quit' to exit")
    print("=" * 70)
    print(f"Assistant ID: {assistant_id}")
    print(f"Thread ID: {thread_id}\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                # Cleanup
                client.delete_assistant(assistant_id)
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Create run
            run = client.create_run(
                thread_id=thread_id,
                assistant_id=assistant_id,
                input_data={
                    "messages": [{"role": "user", "content": user_input}]
                }
            )
            
            # Wait and display
            print("Thinking...", end="", flush=True)
            client.wait_for_run(thread_id, run["run_id"])
            print("\r" + " " * 20 + "\r", end="")
            
            state = client.get_thread_state(thread_id)
            last_message = state.get("values", {}).get("messages", [])[-1]
            print(f"Assistant: {last_message.get('content', '')}\n")
            
        except KeyboardInterrupt:
            client.delete_assistant(assistant_id)
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive()
    else:
        main()
