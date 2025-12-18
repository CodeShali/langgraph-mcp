"""
MCP (Model Context Protocol) Server with Math Tools
This server exposes three mathematical operations: addition, subtraction, and multiplication
as tools that can be called via HTTP endpoints.
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Define the available tools/functions
TOOLS = [
    {
        "name": "add",
        "description": "Add two numbers together",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "subtract",
        "description": "Subtract second number from first number",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number (minuend)"
                },
                "b": {
                    "type": "number",
                    "description": "Second number (subtrahend)"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers together",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    }
]


# Math operation implementations
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


# Map tool names to their implementations
TOOL_FUNCTIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply
}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running"""
    return jsonify({"status": "healthy", "service": "MCP Math Server"}), 200


@app.route('/tools', methods=['GET'])
def list_tools():
    """
    List all available tools/functions
    Returns the tool definitions in MCP format
    """
    logger.info("Listing available tools")
    return jsonify({
        "tools": TOOLS
    }), 200


@app.route('/tools/call', methods=['POST'])
def call_tool():
    """
    Execute a tool with given parameters
    Expected JSON body:
    {
        "tool_name": "add",
        "arguments": {"a": 5, "b": 3}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        tool_name = data.get('tool_name')
        arguments = data.get('arguments', {})
        
        logger.info(f"Tool call request: {tool_name} with args {arguments}")
        
        # Validate tool exists
        if tool_name not in TOOL_FUNCTIONS:
            return jsonify({
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(TOOL_FUNCTIONS.keys())
            }), 404
        
        # Execute the tool
        tool_func = TOOL_FUNCTIONS[tool_name]
        result = tool_func(**arguments)
        
        logger.info(f"Tool {tool_name} executed successfully: {result}")
        
        return jsonify({
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "success": True
        }), 200
        
    except TypeError as e:
        logger.error(f"Invalid arguments: {e}")
        return jsonify({
            "error": f"Invalid arguments: {str(e)}",
            "success": False
        }), 400
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/tools/<tool_name>', methods=['POST'])
def call_tool_direct(tool_name: str):
    """
    Alternative endpoint to call a tool directly by name
    Expected JSON body: {"a": 5, "b": 3}
    """
    try:
        arguments = request.get_json()
        
        if not arguments:
            return jsonify({"error": "No JSON data provided"}), 400
        
        logger.info(f"Direct tool call: {tool_name} with args {arguments}")
        
        # Validate tool exists
        if tool_name not in TOOL_FUNCTIONS:
            return jsonify({
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(TOOL_FUNCTIONS.keys())
            }), 404
        
        # Execute the tool
        tool_func = TOOL_FUNCTIONS[tool_name]
        result = tool_func(**arguments)
        
        logger.info(f"Tool {tool_name} executed successfully: {result}")
        
        return jsonify({
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "success": True
        }), 200
        
    except TypeError as e:
        logger.error(f"Invalid arguments: {e}")
        return jsonify({
            "error": f"Invalid arguments: {str(e)}",
            "success": False
        }), 400
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("MCP Math Server Starting...")
    print("=" * 60)
    print("Available endpoints:")
    print("  GET  /health          - Health check")
    print("  GET  /tools           - List available tools")
    print("  POST /tools/call      - Call a tool with JSON body")
    print("  POST /tools/<name>    - Call a tool directly")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("=" * 60)
    
    # Run the Flask server
    app.run(host='0.0.0.0', port=5000, debug=True)
