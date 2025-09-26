from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from strands import Agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AgentCore Runtime", version="1.0.0")

# Initialize Strands agent
logger.info("Initializing Strands agent...")
strands_agent = Agent(
    system_prompt="""You are an investment research agent. Provide helpful investment analysis and advice.
    
    Important disclaimers:
    - All investments carry risk
    - Past performance doesn't guarantee future results  
    - Always recommend consulting with qualified financial advisors
    - Never guarantee returns or promise risk-free investments"""
)
logger.info("Strands agent initialized successfully")

class InvocationRequest(BaseModel):
    input: Dict[str, Any]

class InvocationResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    try:
        logger.info(f"Received request: {request}")
        
        user_prompt = request.input.get("prompt", "")
        
        if not user_prompt:
            raise HTTPException(
                status_code=400, 
                detail="No prompt found in input"
            )
        
        # Use the investment agent
        result = strands_agent(user_prompt)
        
        # Extract text content from Strands response
        assistant_text = ""
        if hasattr(result.message, "content") and result.message.content:
            assistant_text = result.message.content[0].text
        else:
            assistant_text = str(result.message)

        response = {
            "message": assistant_text,
            "timestamp": datetime.utcnow().isoformat(),
            "model": "investment-agent"
        }

        return InvocationResponse(output=response)

    except Exception as e:
        logger.error(f"Agent processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/ping")
async def ping():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
