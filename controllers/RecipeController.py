from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import Union
from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException

from data import RecipeData 
from data import IngredientData
from schemas import RecipeSchema as schemas
from models import Recipe, Base
from database import engine, SessionLocal


logger = getLogger("recipe-logger")

Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/recipes/createtable")
def create_table(db: SessionLocal = Depends(get_db)):
    RecipeData.create_table(db)
    return {"message": "Recipe Table created successfully"}

@router.get("/recipes/droptable")
def delete_table(db: SessionLocal = Depends(get_db)):
    RecipeData.drop_table(db)
    return {"message": "Recipe Table deleted successfully"}


@router.get("/recipes", response_model=list[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    return RecipeData.get_recipes(db, skip, limit)
    

@router.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):
    db_recipe = RecipeData.get_recipe_by_id(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.post("/recipes", response_model=schemas.Recipe)
async def add_recipe(recipe: schemas.RecipeCreate, db: SessionLocal = Depends(get_db)):
    logger.debug("Adding recipe: %s", recipe)
    return RecipeData.add_recipe(db, recipe)
            

#TODO: Re-add put and delete methods

@router.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def update_recipe(recipe_id: int, recipe: schemas.RecipeCreate, db: SessionLocal = Depends(get_db)):
    try:
        db_recipe = RecipeData.get_recipe_by_id(db, recipe_id)
        if db_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        updated_recipe = RecipeData.update_recipe(db, recipe_id, recipe)
        return updated_recipe
    except Exception as e:
        return {"message": "Unable to update recipe: error: " + str(e)}

# @router.put("/recipes/{recipe_id}")
# async def update_recipe(recipe_id: int, recipe: Recipe):
#     try:
#         updated_recipe = recipe_data.update_recipe(recipe_id, recipe)
#         return updated_recipe
#     except Exception as e:
#         return {"message": "Unable to update recipe: error: " + str(e)}


# @router.delete("/recipes/{recipe_id}")
# async def delete_recipe(recipe_id: int):
#     try:
#         recipe_data.delete_recipe(recipe_id)
#         return {"message": f"Recipe'{recipe_id}' deleted successfully"}
#     except Exception as e:
#         return {"message": "Unable to delete recipe: error: " + str(e)} 
