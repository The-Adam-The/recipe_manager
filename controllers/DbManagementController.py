from fastapi import APIRouter
from data.IngredientData import IngredientData
from data.RecipeData import RecipeData
from logging import getLogger

logger = getLogger("recipe-logger")
logger.info("Creating DbManagementController")

ingredient_data = IngredientData(logger)
recipe_data = RecipeData(logger)
router = APIRouter()

# Db management functions

@router.post("/createrecipetable")
def create_recipes_table():
    recipe_data.create_recipes_table()
    return {"message": "Recipes table created successfully"}

@router.delete("/droprecipes")
def drop_recipes():
    recipe_data.drop_recipes_table()
    return {"message": "Recipes table dropped successfully"}

@router.post("/createingredientstable")
async def create_ingredients_table():
    ingredient_data.create_ingredients_table()
    return {"message": "Ingredients table created successfully"}

@router.delete("/dropingredients")
async def drop_ingredients():
    ingredient_data.drop_ingredients_table()
    return {"message": "Ingredients table dropped successfully"}