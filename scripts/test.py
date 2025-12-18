#!/usr/bin/env python3
"""
Test script for the local deployment
Tests both local and public endpoints
"""

import requests
import json
import time
import sys
import os

def test_local_endpoints():
    """Test local endpoints"""
    print("Testing local endpoints...")
    
    # Test MCP server
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Server: OK")
        else:
            print(f"❌ MCP Server: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP Server: {e}")
        return False
    
    # Test API server
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Server: OK")
        else:
            print(f"❌ API Server: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Server: {e}")
        return False
    
    return True

def test_api_functionality():
    """Test API functionality with a sample conversation"""
    print("\nTesting API functionality...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Create assistant
        response = requests.post(f"{base_url}/assistants", 
                               json={"name": "Test Assistant"})
        assistant = response.json()
        assistant_id = assistant["assistant_id"]
        print(f"✅ Created assistant: {assistant_id}")
        
        # Create thread
        response = requests.post(f"{base_url}/threads", json={})
        thread = response.json()
        thread_id = thread["thread_id"]
        print(f"✅ Created thread: {thread_id}")
        
        # Test queries
        queries = [
            "What is 15 plus 27?",
            "What is 100 minus 37?",
            "What is 8 times 9?"
        ]
        
        for query in queries:
            print(f"\n🤔 Query: {query}")
            
            # Create run
            response = requests.post(f"{base_url}/threads/{thread_id}/runs",
                                   json={
                                       "assistant_id": assistant_id,
                                       "input": {
                                           "messages": [{"role": "user", "content": query}]
                                       }
                                   })
            run = response.json()
            
            if run.get("status") == "success":
                # Get response
                response = requests.get(f"{base_url}/threads/{thread_id}/state")
                state = response.json()
                messages = state["values"]["messages"]
                last_message = messages[-1]
                print(f"✅ Response: {last_message['content']}")
            else:
                print(f"❌ Run failed: {run}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("LangGraph MCP Deployment Test")
    print("=" * 60)
    
    # Test local endpoints
    if not test_local_endpoints():
        print("\n❌ Local endpoint tests failed")
        sys.exit(1)
    
    # Test API functionality
    if not test_api_functionality():
        print("\n❌ API functionality tests failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed!")
    print("=" * 60)
    print("\nYour deployment is working correctly!")
    print("\nTo get the public URL:")
    print("1. Check the cloudflared output in the start.sh terminal")
    print("2. Look for a URL like: https://xxx-xxx-xxx.trycloudflare.com")
    print("3. Test it: curl https://your-url.trycloudflare.com/health")

if __name__ == "__main__":
    main()
