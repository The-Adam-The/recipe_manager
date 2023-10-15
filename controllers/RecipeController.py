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
    recipes = RecipeData.get_recipes(db, skip, limit)
    for recipe in recipes:
        ingredients = IngredientData.get_ingredients_by_recipe_id(db, recipe.id)
        recipe.ingredients = ingredients
    return recipes

@router.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):
    db_recipe = RecipeData.get_recipe_by_id(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    ingredients = IngredientData.get_ingredients_by_recipe_id(db, recipe_id)
    db_recipe.ingredients = ingredients
    return db_recipe


@router.post("/recipes", response_model=schemas.Recipe)
async def add_recipe(input_recipe: schemas.RecipeCreate, db: SessionLocal = Depends(get_db)):
    logger.debug("Adding recipe: %s", input_recipe)
    output_recipe = RecipeData.add_recipe(db, input_recipe)
    output_ingredients = []
    for ingredient in input_recipe.ingredients:
        ingredient.recipe_id = output_recipe.id
        output_ingredients.append(IngredientData.add_ingredient(db, ingredient))
    output_recipe.ingredients = output_ingredients
    return output_recipe


 

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


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):
    try:
        db_recipe = RecipeData.get_recipe_by_id(db, recipe_id)
        if db_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        if RecipeData.delete_recipe(db, recipe_id):
            return {"message": f"Recipe'{recipe_id}' deleted successfully"}
        else:
            return {"message": f"Unable to delete recipe '{recipe_id}'"}
    except Exception as e:
        return {"message": "Unable to delete recipe: error: " + str(e)} 
