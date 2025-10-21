from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.strings.services import DBTasks
from src.strings.models import String
from src.strings.schemas import StringRequest

router = APIRouter()
db_task = DBTasks()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_string(string: StringRequest,session: AsyncSession = Depends(get_session)):
    string_add = await db_task.add_string(string.value, session)

    return string_add

