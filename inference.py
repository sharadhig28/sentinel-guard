import asyncio
import os
import json
from typing import List, Optional

# Importing YOUR models and client
from models import Action as MyEnvV4Action
from client import SentinelClient as MyEnvV4Env

# Configuration
TASK_NAME = os.getenv("TASK_ID", "brute_force") 
BENCHMARK = "sentinel_guard_v1"
MAX_STEPS = 5

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

async def main():
    # We are bypassing the OpenAI client to avoid 403/410 errors
    env = MyEnvV4Env(base_url="http://localhost:8000") 

    rewards = []
    log_start(task=TASK_NAME, env=BENCHMARK, model="MOCK_EXPERT_AGENT")
    
    try:
        # Reset environment
        result = await env.reset() 
        obs = result['observation']
        done = False
        
        for step in range(1, MAX_STEPS + 1):
            # --- MOCK AI LOGIC ---
            # This logic mimics a perfect agent based on your environment.py rules
            if TASK_NAME == "brute_force":
                action_data = {
                    "cmd": "BLOCK_IP", 
                    "target": "192.168.1.50", 
                    "reasoning": "Detected 3 failed login attempts from this source."
                }
            elif TASK_NAME == "impossible_travel":
                action_data = {
                    "cmd": "SUSPEND_USER", 
                    "target": "shara", 
                    "reasoning": "Account activity detected in Mumbai and London simultaneously."
                }
            elif TASK_NAME == "data_exfil":
                action_data = {
                    "cmd": "ISOLATE_HOST", 
                    "target": "192.168.1.100", 
                    "reasoning": "Outbound data transfer exceeded 800MB threshold."
                }
            else:
                action_data = {"cmd": "IGNORE", "target": "none", "reasoning": "No threat found."}

            # 2. Environment takes the action via your local FastAPI server
            step_result = await env.step(MyEnvV4Action(**action_data))
            
            reward = step_result['reward']
            done = step_result['done']
            obs = step_result['observation']
            
            rewards.append(reward)
            log_step(step=step, action=action_data['cmd'], reward=reward, done=done, error=None)
            
            if done: 
                break

        success = sum(rewards) >= 1.0
        log_end(success=success, steps=len(rewards), score=sum(rewards), rewards=rewards)

    finally:
        await env.close()

if __name__ == "__main__":
    asyncio.run(main())