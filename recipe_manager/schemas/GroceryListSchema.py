from pydantic import BaseModel

class GroceryList(BaseModel):
    date: str
    meals: list
    num_meals: int
    ingredients: dict[str, dict]

class GroceryListCreate(BaseModel):
    pass

class GroceryListUpdate(BaseModel):
    date: str
    meals: list
    num_meals: int
    ingredients: dict[str, dict]

    class config:
        orm_mode = True