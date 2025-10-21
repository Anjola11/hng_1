from pydantic import BaseModel


class StringRequest(BaseModel):
    value: str