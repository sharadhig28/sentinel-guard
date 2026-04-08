import sys
import os
from models import Observation, Action, LogEntry

class SentinelEnv:
    def __init__(self):
        self.current_task = "brute_force"
        self.step_count = 0

    def reset(self, task_id: str = "brute_force"):
        self.current_task = task_id
        self.step_count = 0
        
        # Always return a valid Observation object
        return Observation(
            logs=[LogEntry(timestamp="2026-04-08 10:00:00", source_ip="192.168.1.50", message="Failed login attempt", level="WARNING")],
            active_alerts=["High frequency failed logins from 192.168.1.50"]
        )

    def step(self, action: Action):
        self.step_count += 1
        reward = 0.0
        done = False
        
        if self.current_task == "brute_force" and action.cmd == "BLOCK_IP" and action.target == "192.168.1.50":
            reward = 1.0
            done = True
            
        obs = Observation(logs=[], active_alerts=[])
        return obs, reward, done, {}
