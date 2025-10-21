import hashlib
from collections import Counter
from src.strings.models import String
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import DatabaseError

class Properties:

    def is_palindrome(self,string):
        normalised = string.replace(" ","").lower()
        reversed = normalised[::-1]

        return reversed == normalised

    def unique_characters(self,string):
        normalised = string.replace(" ","")
        unique = set(normalised)
    
        return len(unique)

    def word_count(self,string):
        word_list = string.split()

        return len(word_list)

   

    def sha256_hash(self,string):
        encoded = string.encode('utf-8')

        hash = hashlib.sha256(encoded)
        return hash.hexdigest()

 

    def character_frequency_map(self,string):
        count = Counter(string)

        return dict(count)
    
    def all_properties(self,string):
        properties ={
            "length": len(string),
            "is_palindrome": self.is_palindrome(string),
            "unique_characters": self.unique_characters(string),
            "word_count": self.word_count(string),
            "sha256_hash": self.sha256_hash(string),
            "character_frequency_map": self.character_frequency_map(string)
        }

        return properties
    
class DBTasks(Properties):

    async def check_string(self, string, session: AsyncSession):
        statement = select(String).where(String.value == string)
        result = await session.exec(statement)

        return result.first()
    
    async def add_string(self, string_value:str, session: AsyncSession):
        string_exists = await self.check_string(string_value, session)

        if string_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= "String already exists in the system"
            )

        string_properties = self.all_properties(string_value)
    
        new_string = String(value= string_value, **string_properties)

        try:
            
            session.add(new_string)
            await session.commit()
            await session.refresh(new_string)
            return {
                "id": new_string.sha256_hash,
                "value": string_value,
                "properties": string_properties,
                "created_at": new_string.created_at
            }

        except DatabaseError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error: Failed to add string"
            )

        
        

