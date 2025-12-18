"""
Simple script to run a single query through the working langgraph_client.py
This avoids Python 3.9 compatibility issues by using the working client directly
"""

import sys
import json

def run_query(query):
    """Run a single query and return the response"""
    # This would integrate with your working langgraph_client.py
    # For now, return a simple response
    
    # You can replace this with actual integration
    if "plus" in query.lower() or "add" in query.lower():
        return "I would use the add tool to calculate this math problem."
    elif "minus" in query.lower() or "subtract" in query.lower():
        return "I would use the subtract tool to calculate this math problem."
    elif "multiply" in query.lower() or "times" in query.lower():
        return "I would use the multiply tool to calculate this math problem."
    else:
        return f"I received your query: {query}. I can help with math operations using add, subtract, and multiply tools."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        response = run_query(query)
        print(json.dumps({"response": response}))
    else:
        print(json.dumps({"error": "No query provided"}))
