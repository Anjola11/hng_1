from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.strings.services import DBTasks
from src.strings.models import String
from src.strings.schemas import StringRequest
from src.strings.schemas import StringResponse, allStringResponse
from typing import List

router = APIRouter()
db_task = DBTasks()

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=StringResponse)
async def add_string(string: StringRequest,session: AsyncSession = Depends(get_session)):
    string_add = await db_task.add_string(string.value, session)

    return string_add

@router.get("/strings", status_code=status.HTTP_200_OK,response_model=allStringResponse)
async def get_all_strings(session: AsyncSession = Depends(get_session)):
    strings = await db_task.get_all_strings(session)

    return strings


@router.get("/{string_value}", status_code=status.HTTP_200_OK, response_model=StringResponse)
async def get_string(string_value: str, session: AsyncSession = Depends(get_session)):
    string = await db_task.get_string(string_value, session)

    return string

