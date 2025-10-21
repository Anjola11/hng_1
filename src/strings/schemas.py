from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, List

class StringRequest(BaseModel):
    value: str


class StringResponse(BaseModel):
    id: str
    value: str 
    properties: Dict[str, Any]
    created_at: datetime 

class allStringResponse(BaseModel):
    data: List[StringResponse]
    count: int
    filters_applied: dict