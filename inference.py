import asyncio
import os
import json
from typing import List, Optional
from openai import OpenAI

# Importing YOUR models and client
from models import Action as MyEnvAction
from client import SentinelClient as MyEnv

# CHECKLIST RULES 2 & 3: Variables present, defaults ONLY for Base and Model
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN") # NO DEFAULT for token per rule #3

TASK_ID = os.getenv("TASK_ID", "brute_force")
BENCHMARK = "sentinel_guard_v1"
MAX_STEPS = 5

# RULE 5: Structured Logging format (START/STEP/END)
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

async def main():
    # RULE 4: Configure OpenAI client via variables
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    # This points to your live server
    env = MyEnv(base_url="http://localhost:7860") 

    rewards = []
    log_start(task=TASK_ID, env=BENCHMARK, model=MODEL_NAME)
    
    try:
        result = await env.reset() 
        obs = result['observation']
        
        for step in range(1, MAX_STEPS + 1):
            # The judges will provide their own token to run this
            user_prompt = f"Logs: {obs['logs']}\nAlerts: {obs['active_alerts']}\nTake action."
            
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": user_prompt}],
                response_format={ "type": "json_object" }
            )
            
            action_data = json.loads(completion.choices[0].message.content)
            step_result = await env.step(MyEnvAction(**action_data))
            
            reward = step_result['reward']
            done = step_result['done']
            obs = step_result['observation']
            
            rewards.append(reward)
            log_step(step=step, action=action_data['cmd'], reward=reward, done=done, error=None)
            
            if done: break

        log_end(success=sum(rewards) >= 1.0, steps=len(rewards), score=sum(rewards), rewards=rewards)

    finally:
        await env.close()

if __name__ == "__main__":
    asyncio.run(main())
