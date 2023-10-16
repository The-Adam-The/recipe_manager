from pydantic import BaseModel

class GroceryList(BaseModel):
    date: str
    meals: list
    ingredients: dict[str, dict]

class GroceryListCreate(BaseModel):
    pass

class GroceryListUpdate(BaseModel):
    date: str
    meals: list
    ingredients: dict[str, dict]

    class config:
        orm_mode = True