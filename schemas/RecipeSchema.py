from pydantic import BaseModel
from .IngredientSchema import Ingredient


class RecipeBase(BaseModel):
    id: int = None
    name: str
    last_used: str
    date_created: str
    category: str
    # ingredients: list[Ingredient] | None = None
    time_two: int
    time_four: int
    
class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int = None
    name: str
    last_used: str
    date_created: str
    category: str
    ingredients: list[Ingredient] | None = None
    time_two: int
    time_four: int
    
    class Config:
        orm_mode = True