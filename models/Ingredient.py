from pydantic import BaseModel

class Ingredient(BaseModel):
    id: int | None = None
    name: str
    quantity: float
    unit: str
    recipe_id: int | None = None
    perishable: int | None = None