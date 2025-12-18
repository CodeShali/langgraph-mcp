"""
LangGraph Agent for Cloud Deployment
This module defines the agent graph that will be deployed to LangGraph Cloud.
It fetches tools from your MCP server and uses them to answer user queries.
"""

import os
from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
import requests


# Get configuration from environment variables
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:5000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ============================================================================
# State Definition
# ============================================================================

class AgentState(TypedDict):
    """
    State schema for the LangGraph agent.
    - messages: List of conversation messages (with automatic merging via add_messages)
    """
    messages: Annotated[list, add_messages]


# ============================================================================
# MCP Tool Wrappers
# ============================================================================

@tool
def add_numbers(a: float, b: float) -> str:
    """
    Add two numbers together using the MCP server.
    
    Args:
        a: First number to add
        b: Second number to add
    
    Returns:
        String representation of the sum
    """
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/add",
            json={"a": a, "b": b},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"The sum of {a} and {b} is {result['result']}"
    except Exception as e:
        return f"Error calling add tool: {str(e)}"


@tool
def subtract_numbers(a: float, b: float) -> str:
    """
    Subtract second number from first number using the MCP server.
    
    Args:
        a: First number (minuend)
        b: Second number (subtrahend)
    
    Returns:
        String representation of the difference
    """
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/subtract",
            json={"a": a, "b": b},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"The difference of {a} and {b} is {result['result']}"
    except Exception as e:
        return f"Error calling subtract tool: {str(e)}"


@tool
def multiply_numbers(a: float, b: float) -> str:
    """
    Multiply two numbers together using the MCP server.
    
    Args:
        a: First number to multiply
        b: Second number to multiply
    
    Returns:
        String representation of the product
    """
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/multiply",
            json={"a": a, "b": b},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return f"The product of {a} and {b} is {result['result']}"
    except Exception as e:
        return f"Error calling multiply tool: {str(e)}"


# Collect all tools
tools = [add_numbers, subtract_numbers, multiply_numbers]


# ============================================================================
# Agent Node Functions
# ============================================================================

def call_model(state: AgentState) -> dict:
    """
    Node that calls the LLM with the current state and available tools.
    
    Args:
        state: Current agent state containing message history
    
    Returns:
        Dictionary with updated messages
    """
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def call_tools(state: AgentState) -> dict:
    """
    Node that executes the tools requested by the LLM.
    
    Args:
        state: Current agent state containing message history
    
    Returns:
        Dictionary with tool execution results as messages
    """
    last_message = state["messages"][-1]
    tool_messages = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        
        # Find and execute the tool
        tool_func = next((t for t in tools if t.name == tool_name), None)
        if tool_func:
            result = tool_func.invoke(tool_args)
            tool_messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_id,
                    name=tool_name
                )
            )
        else:
            tool_messages.append(
                ToolMessage(
                    content=f"Error: Tool {tool_name} not found",
                    tool_call_id=tool_id,
                    name=tool_name
                )
            )
    
    return {"messages": tool_messages}


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Conditional edge function that determines if we should continue to tools or end.
    
    Args:
        state: Current agent state
    
    Returns:
        "tools" if the last message has tool calls, "end" otherwise
    """
    last_message = state["messages"][-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    return "end"


# ============================================================================
# Initialize LLM and Build Graph
# ============================================================================

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=OPENAI_API_KEY
)

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# Build the agent graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tools)

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

# Compile the graph - this is what gets deployed
graph = workflow.compile()
