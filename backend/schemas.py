from pydantic import BaseModel
from typing import Optional

class Recommendation(BaseModel):
    priority: str
    type: str
    entity_id: str
    title: str
    description: str
    metric: str
    metric_value: float
    evidence: str

class ValidationWarning(BaseModel):
    type: str
    field: str
    count: int