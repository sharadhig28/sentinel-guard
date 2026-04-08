from pydantic import BaseModel, Field
from typing import List, Literal

class LogEntry(BaseModel):
    timestamp: str
    source_ip: str
    user: str
    event: str
    metadata: str

# MAKE SURE THIS IS NAMED 'Observation' (not SOCObservation)
class Observation(BaseModel):
    logs: List[LogEntry] = Field(..., description="System logs for the current window")
    system_health: float = Field(..., description="0.0 to 1.0")
    active_alerts: List[str] = Field(..., description="Current triggered alerts")

# MAKE SURE THIS IS NAMED 'Action' (not SOCAction)
class Action(BaseModel):
    cmd: Literal["BLOCK_IP", "SUSPEND_USER", "ISOLATE_HOST", "IGNORE"]
    target: str = Field(..., description="The IP, Username, or Hostname to act upon")
    reasoning: str = Field(..., description="Short explanation for the action")