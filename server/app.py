from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add root to path so we can find models.py
sys.path.append(os.getcwd())

from models import Action, Observation
from server.environment import SentinelEnv

app = FastAPI()
env = SentinelEnv()

# This tells FastAPI how to read the "task_id" from the checker
class ResetRequest(BaseModel):
    task_id: Optional[str] = "brute_force"

@app.get("/")
async def home():
    return {"message": "SentinelGuard Environment is LIVE"}

@app.post("/reset")
async def reset(request: Optional[ResetRequest] = None):
    # Use the task_id from the checker, or default to brute_force
    task = request.task_id if request else "brute_force"
    obs = env.reset(task_id=task)
    return {"observation": obs}

@app.post("/step")
async def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
async def state():
    return {"status": "running"}
