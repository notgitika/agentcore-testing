# Gitika's AgentCore Testing :)

## Testing Agentcore Runtime primitive

## Files

**Agent Implementation:**
- `src/agents/agent_runtime.py` - FastAPI server with basic agent functionality
- `src/docker/Dockerfile.runtime` - Docker configuration for runtime agent
- `src/docker/pyproject.toml` - Python dependencies

**Build & Deploy:**
- `scripts/build_and_push.sh` - Build and push Docker image to ECR
- Usage: `sh scripts/build_and_push.sh runtime`

**Testing:**
- `tests/test_agent_runtime.py` - Test script for deployed agent
- Usage: `python tests/test_agent_runtime.py`

## Quick Start

1. **Build and deploy:**
   ```bash
   sh scripts/build_and_push.sh runtime
   ```

2. **Update Bedrock AgentCore with new image URI**

3. **Test the deployed agent:**
   ```bash
   python tests/test_agent_runtime.py
   ```

## Configuration

- ECR Repository: `998846730471.dkr.ecr.us-east-1.amazonaws.com/agentcore-test`
- Agent ARN: `arn:aws:bedrock-agentcore:us-east-1:998846730471:runtime/first_testing_agent-qt0qXTEqu4`
