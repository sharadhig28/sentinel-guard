import httpx
from models import Action, Observation

class SentinelClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def reset(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/reset")
            return response.json()

    async def step(self, action: Action):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/step", json=action.dict())
            return response.json()

    async def close(self):
        # Optional: cleanup logic if needed
        pass