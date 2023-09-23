from pydantic import BaseModel
from .Ingredient import Ingredient
class Recipe(BaseModel):
    
    id: int
    name: str
    last_used: str
    date_created: str
    category: str
    ingredients: list[Ingredient]
    time: dict
    