from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from strands import Agent
import logging

from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Strands Agent Server with Native Memory", version="1.0.0")

# Initialize memory client
memory_client = MemoryClient(region_name="us-east-1")
MEMORY_ID = "InvestmentResearchAssistantMemory-mM740qDxze"
logger.info("Using memory ID: {}".format(MEMORY_ID))

class InvocationRequest(BaseModel):
    input: Dict[str, Any]

class InvocationResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    try:
        logger.info("=== REQUEST DEBUG ===")
        logger.info("Received request: {}".format(request))
        
        user_message = request.input.get("prompt", "")
        session_id = request.input.get("sessionId", "default-session")
        actor_id = request.input.get("actorId", "user")
        
        if not user_message:
            raise HTTPException(
                status_code=400, 
                detail="No prompt found in input. Please provide a 'prompt' key in the input."
            )

        # Create AgentCore Memory configuration with retrieval config
        memory_config = AgentCoreMemoryConfig(
            memory_id=MEMORY_ID,
            actor_id=actor_id,
            session_id=session_id,
            retrieval_config={
                # Retrieve from short-term memory (conversation history)
                "/conversations/{actorId}/{sessionId}": RetrievalConfig(
                    top_k=10,
                    relevance_score=0.1  # Low threshold to get all relevant context
                )
            }
        )
        
        # Create session manager with AgentCore Memory
        session_manager = AgentCoreMemorySessionManager(
            agentcore_memory_config=memory_config,
            region_name="us-east-1"
        )
        
        # Create Strands agent with memory session manager
        strands_agent = Agent(
            system_prompt="""You are an investment research agent. Use all you know about the user to provide helpful responses.
            
            Important disclaimers:
            - All investments carry risk
            - Past performance doesn't guarantee future results  
            - Always recommend consulting with qualified financial advisors
            - Never guarantee returns or promise risk-free investments""",
            session_manager=session_manager
        )
        
        logger.info("Strands agent with native memory initialized")
        
        # Process the message - memory should be handled automatically
        result = strands_agent(user_message)
        
        response = {
            "message": result.message,
            "timestamp": datetime.utcnow().isoformat(),
            "model": "strands-agent-with-native-memory",
        }

        return InvocationResponse(output=response)

    except Exception as e:
        logger.error("Agent processing failed: {}".format(str(e)))
        raise HTTPException(status_code=500, detail="Agent processing failed: {}".format(str(e)))

@app.get("/ping")
async def ping():
    logger.info("Health check called")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
