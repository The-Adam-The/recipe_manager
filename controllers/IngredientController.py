from fastapi import APIRouter, HTTPException, Depends
from data import IngredientData as data
from schemas import IngredientSchema as schema
# from models import Ingredient
from database import engine, SessionLocal
from logging import getLogger

logger = getLogger("recipe-logger")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/ingredients/createtable")
async def create_table(db = Depends(get_db)):
    data.create_table(db)
    return {"message": "Table created successfully"}


@router.get("/ingredients/droptable")
async def drop_table(db = Depends(get_db)):
    data.drop_table(db)
    return {"message": "Table deleted successfully"}


@router.get("/ingredients", response_model = list[schema.Ingredient])
async def read_ingredients(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    return data.get_ingredients(db, skip, limit)


@router.get("/ingredients/{ingredient_id}", response_model=schema.Ingredient)
async def read_ingredient(ingredient_id: int, db = Depends(get_db)):
    db_ingredient = data.get_ingredient_by_id(db, ingredient_id)
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient


@router.post("/ingredients", response_model = list[schema.Ingredient])
async def add_ingredient(ingredients: list[schema.Ingredient], db = Depends(get_db)):
    for ingredient in ingredients:
        if ingredient.id is not None:
            if data.get_ingredient_by_id(db, ingredient.id) is not None:
                raise HTTPException(status_code=400, detail="Ingredient already exists")
        data.add_ingredient(db, ingredient)
    return ingredients

#TODO: Readd put and delete methods

@router.put("/ingredients/{ingredient_id}")
async def update_ingredient(ingredient_id: int, ingredient: schema.IngredientCreate, db = Depends(get_db)):
    try:
        updated_ingredient = data.update_ingredient(db, ingredient_id, ingredient)
        return updated_ingredient
    except Exception as e:
        return {"message": "Unable to update ingredient: error: " + str(e)}

@router.delete("/ingredients/{ingredient_id}")
async def delete_ingredient(ingredient_id: int, db = Depends(get_db)):
    try:
        if data.get_ingredient_by_id(db, ingredient_id):
            if data.delete_ingredient(db, ingredient_id):
                return {"message": f"Ingredient'{ingredient_id}' deleted successfully"}
            else:
                return {"message": f"Unable to delete ingredient '{ingredient_id}'"}
    except Exception as e:
        return {"message": "Unable to delete ingredient: error: " + str(e)}