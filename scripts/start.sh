#!/bin/bash

# Start script for LangGraph MCP Local Deployment
# This script starts all required services

set -e

echo "============================================================"
echo "Starting LangGraph MCP Local Deployment"
echo "============================================================"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Source environment variables
source .env

# Check required environment variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set in .env file"
    exit 1
fi

echo "✅ Environment variables loaded"

# Function to start MCP server
start_mcp_server() {
    echo ""
    echo "Starting MCP Server..."
    python3 mcp_server.py &
    MCP_PID=$!
    echo "MCP Server started with PID: $MCP_PID"
    
    # Wait for MCP server to start
    echo "Waiting for MCP server to start..."
    sleep 3
    
    # Test MCP server
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "✅ MCP Server is running at http://localhost:5000"
    else
        echo "❌ MCP Server failed to start"
        exit 1
    fi
}

# Function to start API server
start_api_server() {
    echo ""
    echo "Starting API Server..."
    python3 simple_web_api.py &
    API_PID=$!
    echo "API Server started with PID: $API_PID"
    
    # Wait for API server to start
    echo "Waiting for API server to start..."
    sleep 3
    
    # Test API server
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ API Server is running at http://localhost:8000"
    else
        echo "❌ API Server failed to start"
        exit 1
    fi
}

# Function to expose via tunnel
start_tunnel() {
    echo ""
    echo "Starting Cloudflare Tunnel..."
    
    # Check if cloudflared is installed
    if ! command -v cloudflared &> /dev/null; then
        echo "Installing cloudflared..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install cloudflared
        else
            echo "Please install cloudflared manually: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
            exit 1
        fi
    fi
    
    echo "Exposing API server via Cloudflare Tunnel..."
    cloudflared tunnel --url http://localhost:8000 &
    TUNNEL_PID=$!
    
    echo "Waiting for tunnel to start..."
    sleep 5
    
    echo ""
    echo "🌐 Your API is now publicly accessible!"
    echo "   Check the cloudflared output above for the public URL"
    echo "   It will look like: https://xxx-xxx-xxx.trycloudflare.com"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    if [ ! -z "$MCP_PID" ]; then
        kill $MCP_PID 2>/dev/null || true
        echo "MCP Server stopped"
    fi
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
        echo "API Server stopped"
    fi
    if [ ! -z "$TUNNEL_PID" ]; then
        kill $TUNNEL_PID 2>/dev/null || true
        echo "Tunnel stopped"
    fi
    echo "Cleanup complete"
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

# Start services
start_mcp_server
start_api_server
start_tunnel

echo ""
echo "============================================================"
echo "All services are running!"
echo "============================================================"
echo "Services:"
echo "  📊 MCP Server:  http://localhost:5000"
echo "  🚀 API Server:  http://localhost:8000"
echo "  🌐 Public URL:  Check cloudflared output above"
echo ""
echo "Test your deployment:"
echo "  curl http://localhost:8000/health"
echo "  python3 scripts/test.py"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================================"

# Keep script running
wait
