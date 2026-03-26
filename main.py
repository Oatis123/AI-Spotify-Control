from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

from agent.agent import request_to_agent

# Configure logging for the agent and other modules
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

app = FastAPI(
    title="Spotify Agent API",
    description="Microservice for controlling Spotify through an AI agent",
    version="1.0.0"
)

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    status: str
    result: str

@app.get("/ping", tags=["Health"])
async def ping():
    return {"status": "ok", "message": "Spotify Agent is alive and kicking"}

@app.post("/execute", response_model=CommandResponse, tags=["Agent"])
async def execute_spotify_command(request: CommandRequest):
    try:
        agent_response = request_to_agent(request=request.command)
        
        agent_output = f"Agent successfully processed the command: '{request.command}'"
        
        return CommandResponse(
            status="success",
            result=agent_output
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)