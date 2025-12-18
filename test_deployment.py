"""
Test script for deployed LangGraph Cloud agent.
Update DEPLOYMENT_URL and ASSISTANT_ID after deployment.
"""

import os
from dotenv import load_dotenv
from langraph_cloud_client import LangGraphCloudClient

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION - UPDATE THESE AFTER DEPLOYMENT
# ============================================================================

# Get these from LangSmith after deployment
DEPLOYMENT_URL = "https://YOUR_DEPLOYMENT.langchain.app"  # Replace with your deployment URL
ASSISTANT_ID = "asst_YOUR_ASSISTANT_ID"  # Replace with your assistant ID

# From .env file
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# ============================================================================
# Test Functions
# ============================================================================

def test_deployment():
    """
    Test the deployed agent with sample queries.
    """
    if "YOUR_DEPLOYMENT" in DEPLOYMENT_URL or "YOUR_ASSISTANT" in ASSISTANT_ID:
        print("=" * 70)
        print("ERROR: Please update DEPLOYMENT_URL and ASSISTANT_ID first!")
        print("=" * 70)
        print("\nSteps:")
        print("1. Deploy to LangGraph Cloud (see DEPLOYMENT.md)")
        print("2. Get your deployment URL from LangSmith")
        print("3. Create an assistant and get the assistant ID")
        print("4. Update DEPLOYMENT_URL and ASSISTANT_ID in this file")
        print("5. Run this script again")
        return
    
    if not LANGSMITH_API_KEY:
        print("ERROR: LANGSMITH_API_KEY not set in .env file")
        return
    
    print("=" * 70)
    print("Testing LangGraph Cloud Deployment")
    print("=" * 70)
    print(f"Deployment URL: {DEPLOYMENT_URL}")
    print(f"Assistant ID: {ASSISTANT_ID}")
    print("=" * 70)
    
    # Initialize client
    client = LangGraphCloudClient(
        api_key=LANGSMITH_API_KEY,
        base_url=DEPLOYMENT_URL
    )
    
    # Create thread
    print("\n1. Creating conversation thread...")
    thread = client.create_thread(metadata={"test": "deployment"})
    thread_id = thread["thread_id"]
    print(f"   Thread ID: {thread_id}")
    
    # Test queries
    queries = [
        "What is 15 plus 27?",
        "Now multiply that result by 2",
        "What is 100 minus 37?"
    ]
    
    print("\n2. Running test queries...")
    for i, query in enumerate(queries, 1):
        print(f"\n   Query {i}: {query}")
        
        # Create run
        run = client.create_run(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            input_data={
                "messages": [
                    {"role": "user", "content": query}
                ]
            }
        )
        
        # Wait for completion
        print("   Waiting for response...", end="", flush=True)
        completed_run = client.wait_for_run(thread_id, run["run_id"], timeout=30)
        print("\r" + " " * 30, end="\r")
        
        # Get response
        state = client.get_thread_state(thread_id)
        last_message = state.get("values", {}).get("messages", [])[-1]
        print(f"   Response: {last_message.get('content', 'No response')}")
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print(f"\nView traces at: https://smith.langchain.com")
    print(f"Thread ID: {thread_id}")


def interactive_test():
    """
    Interactive mode to chat with the deployed agent.
    """
    if "YOUR_DEPLOYMENT" in DEPLOYMENT_URL or "YOUR_ASSISTANT" in ASSISTANT_ID:
        print("ERROR: Please update DEPLOYMENT_URL and ASSISTANT_ID first!")
        return
    
    if not LANGSMITH_API_KEY:
        print("ERROR: LANGSMITH_API_KEY not set")
        return
    
    client = LangGraphCloudClient(
        api_key=LANGSMITH_API_KEY,
        base_url=DEPLOYMENT_URL
    )
    
    # Create thread
    thread = client.create_thread()
    thread_id = thread["thread_id"]
    
    print("\n" + "=" * 70)
    print("Interactive Mode - Deployed Agent")
    print("=" * 70)
    print(f"Deployment: {DEPLOYMENT_URL}")
    print(f"Assistant: {ASSISTANT_ID}")
    print(f"Thread: {thread_id}")
    print("\nType 'quit' to exit")
    print("=" * 70 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Create run
            run = client.create_run(
                thread_id=thread_id,
                assistant_id=ASSISTANT_ID,
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
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_test()
    else:
        test_deployment()
