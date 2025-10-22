from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.strings.services import DBTasks
from src.strings.models import String
from src.strings.schemas import StringRequest
from src.strings.schemas import StringResponse, allStringResponse
from src.strings.schemas import NaturalLanguageResponse
from pydantic import ValidationError

router = APIRouter()
db_task = DBTasks()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StringResponse)
async def add_string(string: StringRequest, session: AsyncSession = Depends(get_session)):
    string_add = await db_task.add_string(string.value, session)
    return string_add

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
