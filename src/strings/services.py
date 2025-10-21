import hashlib
from collections import Counter

class Properties:

    def is_palindrome(self,string):
        normalised = string.replace(" ","")
        reversed = normalised[::-1]

        return reversed == string

    def unique_characters(self,string):
        normalised = string.replace(" ","")
        unique = set(normalised)
    
        return len(unique)

    def word_count(self,string):
        word_list = string.split(" ")

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
            "string": string,
            "length": len(string),
            "is_palindrome": self.is_palindrome(string),
            "unique_characters": self.unique_characters(string),
            "word_count": self.word_count(string),
            "sha256_hash": self.sha256_hash(string),
            "character_frequency_map": self.character_frequency_map(string)
        }

        return properties
    



