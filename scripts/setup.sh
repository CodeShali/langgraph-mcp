#!/bin/bash

# Setup script for LangGraph MCP Local Deployment
# Run this script to set up the project on a new machine

set -e

echo "============================================================"
echo "LangGraph MCP Local Deployment Setup"
echo "============================================================"

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY=your-openai-key"
    echo "   - LANGSMITH_API_KEY=your-langsmith-key (optional)"
    echo "   - MCP_SERVER_URL will be set automatically"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: ./scripts/start.sh"
echo "============================================================"
