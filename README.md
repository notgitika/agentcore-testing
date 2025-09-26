# Gitika's AgentCore Testing :)

## Testing Agentcore Runtime primitive

## Files

**Agent Implementation:**
- `src/agents/agent_runtime.py` - FastAPI server with basic agent functionality
- `src/agents/agent_native_memory.py` - Agent with native memory integration using AgentCoreMemorySessionManager
- `src/agents/agent_with_built_in_tools.py` - Flask app with built-in code interpreter tool
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
- `tests/test_code_interpreter.py` - Test script for code interpreter functionality
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

### Code Interpreter Agent
1. **Run locally:**
   ```bash
   cd src/agents
   python agent_with_built_in_tools.py
   ```

2. **Test code interpreter functionality:**
   ```bash
   python tests/test_code_interpreter.py
   # Use http://localhost:8080 when prompted for endpoint
   ```

## Memory Integration

The native memory agent uses `AgentCoreMemorySessionManager` which:
- Automatically saves conversation history to AgentCore Memory
- Retrieves relevant context for each interaction
- Provides transparent memory management without manual tool calls

## Code Interpreter Integration

The code interpreter agent uses `CodeInterpreter` from `bedrock_agentcore.tools` which:
- Executes Python code in a secure sandbox environment
- Handles portfolio calculations and data analysis
- Maintains separate code execution sessions per user

## Configuration

- ECR Repository: `998846730471.dkr.ecr.us-east-1.amazonaws.com/agentcore-test`
- Agent ARN: `arn:aws:bedrock-agentcore:us-east-1:998846730471:runtime/first_testing_agent-qt0qXTEqu4`
- Memory ID: `TestMemory_20250926064545-57A2248i7b`
