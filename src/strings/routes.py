from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.strings.services import DBTasks
from src.strings.schemas import StringRequest, StringResponse, allStringResponse, NaturalLanguageResponse
import json
from datetime import datetime

router = APIRouter()
db_task = DBTasks()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("", status_code=status.HTTP_201_CREATED)
async def add_string(string: StringRequest, session: AsyncSession = Depends(get_session)):
    string_add = await db_task.add_string(string.value, session)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json.loads(json.dumps(string_add, default=json_serial))
    )


@router.get("/filter-by-natural-language", status_code=status.HTTP_200_OK, response_model=NaturalLanguageResponse)
async def filter_by_nl(query: str, session: AsyncSession = Depends(get_session)):
    results = await db_task.parse_natural_query(query, session=session)
    return results


@router.get("/", status_code=status.HTTP_200_OK, response_model=allStringResponse)
async def get_all_strings(
    is_palindrome: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    word_count: int | None = None,
    contains_character: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    strings = await db_task.get_all_strings(
        is_palindrome,
        min_length,
        max_length,
        word_count,
        contains_character,
        session
    )
    return strings


@router.get("/{string_value}", status_code=status.HTTP_200_OK, response_model=StringResponse)
async def get_string(string_value: str, session: AsyncSession = Depends(get_session)):
    string = await db_task.get_string(string_value, session)
    return string


@router.delete("/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_string(string_value: str, session: AsyncSession = Depends(get_session)):
    await db_task.delete_string(string_value, session)
    return None