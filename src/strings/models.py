from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, timezone
from typing import Dict, Any

def utc_now():
    return datetime.now(timezone.utc)

class String(SQLModel, table=True):
    __tablename__ = "strings"

    id: str = Field(primary_key=True)
    value: str = Field(index=True)
    properties: Dict[str, Any] = Field(sa_column=Column(pg.JSONB))
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(pg.TIMESTAMP(timezone=True))
        )