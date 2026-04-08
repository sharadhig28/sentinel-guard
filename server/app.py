from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# This ensures we can find models and environment logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from environment import SentinelEnv
    from models import Action, Observation
except ImportError:
    from server.environment import SentinelEnv
    from models import Action, Observation

app = FastAPI(title="SentinelGuard RL Environment")
env = SentinelEnv()

@app.get("/")
async def home():
    return {"message": "SentinelGuard Environment is LIVE", "docs": "/docs", "status_endpoint": "/state"}

@app.post("/reset")
async def reset():
    obs = env.reset()
    # Ensure we return a dictionary
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
    return {"status": "running", "task": env.current_task}
