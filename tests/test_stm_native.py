#!/usr/bin/env python3

from strands import Agent
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from datetime import datetime

print("=== Testing Short-Term Memory with Native Integration ===")

# Create a fresh memory for STM testing
client = MemoryClient(region_name="us-east-1")
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
try:
    basic_memory = client.create_memory(
        name=f"STMTestMemory_{timestamp}",
        description="Basic memory for testing short-term functionality"
    )
    MEM_ID = basic_memory.get('id')
    print(f"Created memory: {MEM_ID}")
except Exception as e:
    print(f"Using existing memory: {e}")
    # Use existing memory
    memories = list(client.list_memories())
    for memory in memories:
        if "STMTestMemory" in memory.get('name', ''):
            MEM_ID = memory.get('id')
            print(f"Using existing memory: {MEM_ID}")
            break

# Use unique IDs for this test
ACTOR_ID = "test_actor_{}".format(datetime.now().strftime("%Y%m%d%H%M%S"))
SESSION_ID = "test_session_{}".format(datetime.now().strftime("%Y%m%d%H%M%S"))

print(f"Actor ID: {ACTOR_ID}")
print(f"Session ID: {SESSION_ID}")

# Configure memory (no retrieval_config for basic STM)
agentcore_memory_config = AgentCoreMemoryConfig(
    memory_id=MEM_ID,
    session_id=SESSION_ID,
    actor_id=ACTOR_ID
)

# Create session manager
session_manager = AgentCoreMemorySessionManager(
    agentcore_memory_config=agentcore_memory_config,
    region_name="us-east-1"
)

# Create agent
agent = Agent(
    system_prompt="You are a helpful assistant. Use all you know about the user to provide helpful responses.",
    session_manager=session_manager,
)

print("\n=== Testing Conversation ===")

# Test conversation
print("\n1. First message:")
response1 = agent("I prefer conservative, low-risk tech stocks")
print(f"Agent: {response1}")

print("\n2. Second message:")
response2 = agent("What preferences did I just mention to you?")
print(f"Agent: {response2}")

print("\n=== STM Test Complete ===")
