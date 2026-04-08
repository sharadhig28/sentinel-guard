import random
import sys
import os
# This tells Python to look one folder up for models.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Observation, Action, LogEntry
class SentinelEnv:
    def __init__(self):
        self.tasks = ["brute_force", "impossible_travel", "data_exfil"]
        self.current_task = "brute_force"
        self.step_count = 0
        self.max_steps = 5
        self.is_done = False

    def reset(self, task_id: str = "brute_force"):
        self.current_task = task_id
        self.step_count = 0
        self.is_done = False
        return self._get_obs()

    def _get_obs(self):
        # Easy Task Logs
        if self.current_task == "brute_force":
            logs = [
                LogEntry(timestamp="10:00", source_ip="192.168.1.50", user="root", event="failed_login", metadata="Try 1"),
                LogEntry(timestamp="10:01", source_ip="192.168.1.50", user="root", event="failed_login", metadata="Try 2")
            ]
            alerts = ["Brute Force Detected"]
        
        # Medium Task Logs
        elif self.current_task == "impossible_travel":
            logs = [
                LogEntry(timestamp="10:00", source_ip="1.1.1.1", user="alice", event="login", metadata="Location: India"),
                LogEntry(timestamp="10:05", source_ip="2.2.2.2", user="alice", event="login", metadata="Location: USA")
            ]
            alerts = ["Impossible Travel Detected"]

        # Hard Task Logs
        else:
            logs = [
                LogEntry(timestamp="10:00", source_ip="192.168.1.100", user="sys_srv", event="outbound_data", metadata="Size: 500MB"),
            ]
            alerts = ["Unusual Data Volume"]

        return Observation(logs=logs, system_health=0.8, active_alerts=alerts)

    def step(self, action: Action):
        self.step_count += 1
        reward = 0.0
        
        # Grader Logic
        if self.current_task == "brute_force":
            if action.cmd == "BLOCK_IP" and action.target == "192.168.1.50":
                reward = 1.0
            elif action.cmd == "IGNORE":
                reward = -0.2 # Penalty for letting the attack continue
        
        # Task 2 Success
        elif self.current_task == "impossible_travel":
            if action.cmd == "SUSPEND_USER" and action.target == "shara":
                reward = 1.0
            elif action.cmd == "BLOCK_IP":
                reward = 0.5 # Partial credit for blocking the IP, but user account is still compromised
        
        # Task 3 Success
        elif self.current_task == "data_exfil":
            if action.cmd == "ISOLATE_HOST" and action.target == "192.168.1.100":
                reward = 1.0
        
        # Set done if task is solved or time is up
        if reward >= 1.0 or self.step_count >= self.max_steps:
            self.is_done = True

        return self._get_obs(), reward, self.is_done, {"msg": f"Step {self.step_count} completed"}
