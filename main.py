from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

from agent.agent import request_to_agent

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

def run_agent_task(command: str):
    try:
        request_to_agent(request=command)
    except Exception as e:
        logging.error(f"Agent background task failed: {str(e)}")

@app.get("/ping", tags=["Health"])
async def ping():
    return {"status": "ok", "message": "Spotify Agent is alive and kicking"}

@app.post("/execute", response_model=CommandResponse, tags=["Agent"])
async def execute_spotify_command(request: CommandRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_agent_task, request.command)
    
    return CommandResponse(
        status="accepted",
        result=f"Command '{request.command}' accepted for background processing"
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=False)