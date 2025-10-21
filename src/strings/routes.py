from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.strings.services import Properties
from src.strings.models import String

router = APIRouter()
properties = Properties()

@router.post("/{string}")
async def add_string(string,session: AsyncSession = Depends(get_session)):
    string_properties = properties.all_properties(string)
    
    new_string = String(**string_properties)

    session.add(new_string)
    await session.commit()

    return {
        "id": new_string.sha256_hash,
        "value": string,
        "properties": string_properties,
        "created_at": new_string.created_at
    }

