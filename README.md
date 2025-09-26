# Gitika's AgentCore Testing :)

## Testing Agentcore Runtime primitive

## Files

**Agent Implementation:**
- `src/agents/agent_runtime.py` - FastAPI server with basic agent functionality
- `src/agents/agent_native_memory.py` - Agent with native memory integration using AgentCoreMemorySessionManager
- `src/docker/Dockerfile.runtime` - Docker configuration for runtime agent
- `src/docker/Dockerfile.native` - Docker configuration for native memory agent
- `src/docker/pyproject.toml` - Python dependencies

**Build & Deploy:**
- `scripts/build_and_push.sh` - Build and push Docker image to ECR
- Usage: 
  - `sh scripts/build_and_push.sh runtime` - Deploy basic agent
  - `sh scripts/build_and_push.sh native` - Deploy memory agent

**Testing:**
- `tests/test_agent_runtime.py` - Test script for deployed agent
- `test_memory_primitive.py` - Test script for memory functionality
- Usage: `python tests/test_agent_runtime.py`

## Quick Start

### Basic Runtime Agent
1. **Build and deploy:**
   ```bash
   sh scripts/build_and_push.sh runtime
   ```

2. **Update Bedrock AgentCore with new image URI**

3. **Test the deployed agent:**
   ```bash
   python tests/test_agent_runtime.py
   ```

### Memory Agent
1. **Build and deploy:**
   ```bash
   sh scripts/build_and_push.sh native
   ```

2. **Update Bedrock AgentCore with new image URI**

3. **Test memory functionality:**
   ```bash
   python test_memory_primitive.py
   ```

## Memory Integration

The native memory agent uses `AgentCoreMemorySessionManager` which:
- Automatically saves conversation history to AgentCore Memory
- Retrieves relevant context for each interaction
- Provides transparent memory management without manual tool calls

## Configuration

- ECR Repository: `998846730471.dkr.ecr.us-east-1.amazonaws.com/agentcore-test`
- Agent ARN: `arn:aws:bedrock-agentcore:us-east-1:998846730471:runtime/first_testing_agent-qt0qXTEqu4`
- Memory ID: `TestMemory_20250926064545-57A2248i7b`
