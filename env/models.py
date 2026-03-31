from pydantic import BaseModel
from typing import List


class Instance(BaseModel):
    id: int
    status: str
    cpu_usage: float
    cost: float


class Observation(BaseModel):
    instances: List[Instance]
    total_cost: float


class Action(BaseModel):
    action_type: str
    instance_id: int


class Reward(BaseModel):
    score: float
