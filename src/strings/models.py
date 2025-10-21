from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, timezone
from typing import Dict, Any

def utc_now():
    return datetime.now(timezone.utc)

class String(SQLModel, table=True):
    __tablename__ = "strings"

    sha256_hash: str = Field(unique=True, index=True, primary_key=True)
    value: str
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    character_frequency_map: Dict[str, Any] = Field(sa_column=Column(pg.JSONB))
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(pg.TIMESTAMP(timezone=True))
        )