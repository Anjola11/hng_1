from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, List

class StringRequest(BaseModel):
    value: str

class DBStringResponse(BaseModel):
    id: str
    value: str 
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: dict
    created_at: datetime 

class StringResponse(BaseModel):
    id: str
    value: str 
    properties: Dict[str, Any]
    created_at: datetime 

class allStringResponse(BaseModel):
    data: List[StringResponse]
    count: int
    filters_applied: dict
    
class InterpretedQueryResponse(BaseModel):
    original: str
    parsed_filters: Dict[str, Any]


class NaturalLanguageResponse(BaseModel):
    data: List[StringResponse]
    count: int
    interpreted_query: InterpretedQueryResponse