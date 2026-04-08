from fastapi import FastAPI, Request
import sys
import os

# Force the root directory into the path so it CANNOT miss models.py
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from models import Action
from server.environment import SentinelEnv

app = FastAPI()
env = SentinelEnv()

@app.get("/")
async def home():
    return {"message": "SentinelGuard Environment is LIVE"}

@app.post("/reset")
async def reset(request: Request):
    # SAFETY NET: Try to get task_id, but don't crash if body is missing/weird
    task_id = "brute_force"
    try:
        body = await request.json()
        task_id = body.get("task_id", "brute_force")
    except:
        pass 
        
    obs = env.reset(task_id=task_id)
    # Force convert to dict so FastAPI doesn't have to guess
    return {"observation": obs.dict() if hasattr(obs, 'dict') else obs}

@app.post("/step")
async def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict() if hasattr(obs, 'dict') else obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
async def state():
    return {"status": "running"}
