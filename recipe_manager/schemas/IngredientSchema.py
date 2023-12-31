from pydantic import BaseModel

class IngredientBase(BaseModel):
    id: int | None = None
    name: str
    quantity: float
    unit: str
    recipe_id: int | None
    recipe: str | None = None
    perishable: int | None = None


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int | None = None
    name: str
    quantity: float
    unit: str
    recipe_id: int | None
    recipe: str | None = None
    perishable: int | None = None
    
    class Config:
        orm_mode = True