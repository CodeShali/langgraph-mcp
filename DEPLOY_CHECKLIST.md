# Deployment Checklist

Follow these steps to deploy your agent to LangGraph Cloud.

## ✅ Pre-Deployment Checklist

- [ ] MCP server is running: `python3 mcp_server.py`
- [ ] MCP server is publicly accessible (ngrok running)
- [ ] Test MCP server: `curl https://your-ngrok-url/tools`
- [ ] LangSmith API key is in `.env`
- [ ] OpenAI API key is in `.env`
- [ ] All files are ready:
  - [ ] `agent_graph.py`
  - [ ] `langgraph.json`
  - [ ] `requirements.txt`

## 📦 Deployment Method: GitHub (Recommended)

### Step 1: Create GitHub Repository

```bash
cd /Users/shashankshali/Desktop/langraph

# Initialize git
git init

# Add .gitignore
cat > .gitignore << 'EOF'
.env
venv/
__pycache__/
*.pyc
.DS_Store
EOF

# Add files
git add agent_graph.py langgraph.json requirements.txt mcp_server.py test_mcp_server.py README.md QUICKSTART.md .gitignore

# Commit
git commit -m "Initial commit: LangGraph MCP integration"
```

### Step 2: Push to GitHub

```bash
# Create a new repository on GitHub: https://github.com/new
# Name it: langgraph-mcp
# Then:

git remote add origin https://github.com/YOUR_USERNAME/langgraph-mcp.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy via LangSmith

1. Go to https://smith.langchain.com
2. Click **Deployments** → **New Deployment**
3. Choose **GitHub**
4. Authorize GitHub access
5. Select repository: `langgraph-mcp`
6. Select branch: `main`
7. LangSmith detects `langgraph.json` ✅

### Step 4: Configure Environment Variables

In deployment settings, add:

```
OPENAI_API_KEY=<your-openai-api-key>

MCP_SERVER_URL=https://c815fb751ca0.ngrok-free.app
```

⚠️ **Update MCP_SERVER_URL with your current ngrok URL!**

### Step 5: Deploy

Click **Deploy** and wait (~2-3 minutes)

### Step 6: Get Deployment Info

After successful deployment, copy:
- **Deployment URL**: `https://xxxxx.langchain.app`
- **Graph ID**: `agent` (from langgraph.json)

### Step 7: Create Assistant

**Option A: Via LangSmith UI**
1. Go to your deployment page
2. Click **Create Assistant**
3. Name: "MCP Math Assistant"
4. Copy the **Assistant ID**: `asst_xxxxx`

**Option B: Via API**
```bash
curl -X POST "https://YOUR_DEPLOYMENT.langchain.app/assistants" \
  -H "x-api-key: YOUR_LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "agent",
    "name": "MCP Math Assistant"
  }'
```

## 🧪 Testing

### Step 1: Update test_deployment.py

Edit `test_deployment.py`:
```python
DEPLOYMENT_URL = "https://YOUR_ACTUAL_DEPLOYMENT.langchain.app"
ASSISTANT_ID = "asst_YOUR_ACTUAL_ID"
```

### Step 2: Run Tests

```bash
# Run automated tests
python3 test_deployment.py

# Or interactive mode
python3 test_deployment.py interactive
```

### Step 3: Verify in LangSmith

1. Go to https://smith.langchain.com
2. Navigate to your deployment
3. Click **Traces** to see execution logs
4. Verify MCP server calls are working

## 🎯 Success Criteria

- [ ] Deployment shows "Running" status in LangSmith
- [ ] Assistant created successfully
- [ ] Test queries return correct responses
- [ ] Traces show MCP server calls
- [ ] No errors in deployment logs

## 🔧 Troubleshooting

### Build Failed
- Check `requirements.txt` for typos
- View build logs in LangSmith
- Ensure `langgraph.json` is valid

### Runtime Errors
- Verify `MCP_SERVER_URL` is correct
- Check ngrok is still running
- Test MCP server: `curl https://your-ngrok-url/health`

### No Response from Assistant
- Check traces in LangSmith
- Verify environment variables are set
- Check OpenAI API key is valid

## 📝 After Deployment

1. **Save your deployment info:**
   ```
   Deployment URL: https://xxxxx.langchain.app
   Assistant ID: asst_xxxxx
   Graph ID: agent
   ```

2. **Update your application code** to use these values

3. **Monitor usage** in LangSmith dashboard

4. **For production:**
   - Deploy MCP server to a permanent URL (not ngrok)
   - Set up monitoring and alerts
   - Configure rate limiting

## 🔄 Updating Deployment

When you change `agent_graph.py`:

```bash
git add agent_graph.py
git commit -m "Update agent logic"
git push
```

LangSmith auto-deploys on push! ✨

## 📚 Resources

- **Deployment Guide**: See DEPLOYMENT.md
- **LangSmith Docs**: https://docs.smith.langchain.com
- **LangGraph Cloud**: https://langchain-ai.github.io/langgraph/cloud/
