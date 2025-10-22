import hashlib
from collections import Counter
from src.strings.models import String
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import DatabaseError
from src.strings.schemas import DBStringResponse
from typing import Dict, Any
import re
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
    def get_string_properties(self, string: DBStringResponse):
        properties = {
            "length": string.length,
            "is_palindrome": string.is_palindrome,
            "unique_characters": string.unique_characters,
            "word_count": string.word_count,
            "sha256_hash": string.sha256_hash,
            "character_frequency_map": string.character_frequency_map
        }
        return properties
    
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
    
        new_string = String(id=string_properties.get("sha256_hash"),
                            value= string_value,
                            **string_properties)

        try:
            
            session.add(new_string)
            await session.commit()
            await session.refresh(new_string)
            return {
                "id": new_string.id,
                "value": new_string.value,
                "properties": string_properties,
                "created_at": new_string.created_at
            }

        except DatabaseError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error: Failed to add string"
            )

    async def get_string(self, string, session:AsyncSession):
        string_value = await self.check_string(string, session)

        if string_value:
            string_value_properties = self.get_string_properties(string_value)
            return {
                "id": string_value.id,
                "value": string_value.value,
                "properties": string_value_properties,
                "created_at": string_value.created_at
            }
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system."
        )
    

    async def get_all_strings(self, 
                              is_palindrome: bool | None, 
                              min_length: int | None,
                              max_length: int | None,
                              word_count: int | None,
                              contains_character: str | None, 
                              session: AsyncSession):
        statement = select(String)
        filters_applied = {}

        if is_palindrome is not None:
            statement = statement.where(String.is_palindrome == is_palindrome)
            filters_applied["is_palindrome"] = is_palindrome
        if min_length is not None:
            statement = statement.where(String.length >= min_length)
            filters_applied["min_length"] = min_length
        if max_length is not None:
            statement = statement.where(String.length <= max_length)
            filters_applied["max_length"] = max_length
        if word_count is not None:
            statement = statement.where(String.word_count == word_count)
            filters_applied["word_count"] = word_count
        if contains_character is not None:
            statement = statement.where(String.value.ilike(f"%{contains_character}%"))
            filters_applied["contains_character"] = contains_character

        result = await session.exec(statement)
        string_object = result.all()

        result_list = []
        for string_value in string_object:
            string_value_properties = self.get_string_properties(string_value)
            result_list.append({
                "id": string_value.id,
                "value": string_value.value,
                "properties": string_value_properties,
                "created_at": string_value.created_at
            })
        return {
            "data": result_list,
            "count": len(result_list),
            "filters_applied": filters_applied
        }
    
    async def parse_natural_query(self, query: str, session:AsyncSession) -> Dict[str, Any]:
        
            normalized_query = query.lower()
            parsed_filters = {}
            
            
            # Check for Palindrome
            if "palindromic" in normalized_query or "palindrome" in normalized_query:
                parsed_filters["is_palindrome"] = True

            # Check for Exact Word Count (Simple Heuristics)
            if "single word" in normalized_query or "one word" in normalized_query:
                parsed_filters["word_count"] = 1
            elif "two words" in normalized_query:
                parsed_filters["word_count"] = 2
            
            # Pattern: looks for 'longer than 10' or 'shorter than 5', grabbing the number
            length_match = re.search(r'(longer than|shorter than|at least|at most|exactly) (\d+)', normalized_query)
            
            if length_match:
                operator = length_match.group(1)
                number = int(length_match.group(2))
                
                if "longer than" in operator or "at least" in operator:
                
                    parsed_filters["min_length"] = number + 1 if "longer than" in operator else number
                
                elif "shorter than" in operator or "at most" in operator:
                    
                    parsed_filters["max_length"] = number - 1 if "shorter than" in operator else number
                
                elif "exactly" in operator:
                    # Check for 'exactly N characters'
                    if "character" in normalized_query or "length" in normalized_query:
                        parsed_filters["min_length"] = number
                        parsed_filters["max_length"] = number

                    # Check for 'exactly N words'
                    if "word" in normalized_query:
                        parsed_filters["word_count"] = number

        
            
            #'first vowel' -> 'a'
            if "first vowel" in normalized_query:
                parsed_filters["contains_character"] = 'a'
            
            #'containing the letter X' or 'contains X'
            char_match = re.search(r'(letter|char|contains) (?:the )?(\w)', normalized_query)
            if char_match:
                
                parsed_filters["contains_character"] = char_match.group(2)


            if not parsed_filters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unable to parse natural language query. No recognizable filters or properties found."
                )

        
            if "min_length" in parsed_filters and "max_length" in parsed_filters:
                if parsed_filters["min_length"] > parsed_filters["max_length"]:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Query parsed but resulted in conflicting length filters (minimum is greater than maximum)."
                    )
            results = await self.get_all_strings(session=session, **parsed_filters)
            return {
                "data": results["data"],
                "count": results["count"],
                "interpreted_query": {
                    "original": query,
                    "parsed_filters": parsed_filters
                }
            }

    async def delete_string(self,string_value:str, session:AsyncSession):
        string = self.get_string(string_value, session)

        if string:
            statement = delete(String).where(String.value == string_value)

            await session.exec(statement)

            await session.commit()

            return {}
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system."
        )

