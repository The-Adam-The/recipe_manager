from logging import getLogger, StreamHandler, DEBUG, Formatter
from typing import Union
from fastapi import FastAPI, Request, APIRouter
import uvicorn
from data.RecipeData import RecipeData
from data.IngredientData import IngredientData 
from models.Recipe import Recipe
from models.Ingredient import Ingredient
from pprint import pprint
from json import JSONDecodeError
import datetime
import sys


logger = getLogger("recipe-logger")
router = APIRouter()

recipe_data = RecipeData(logger)
ingredient_data = IngredientData(logger)

@router.get("/recipes")
def read_recipes():
    try:
        recipes: list[dict] = recipe_data.get_all_recipes()
        for recipe in recipes:
            recipe["ingredients"] = ingredient_data.get_ingredients_by_recipe_id(recipe["id"])
        return recipes
    except Exception as e:
        return {"message": "Unable to get recipes: error: " + str(e)}


@router.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int):
    try:
        recipe = recipe_data.get_recipe_by_id(recipe_id)
        recipe["ingredients"] = ingredient_data.get_ingredients_by_recipe_id(recipe_id)
        return recipe
    except Exception as e:
        return {"message": "Unable to get recipe: error: " + str(e)}
    

@router.post("/recipes")
async def add_recipe(recipe: Recipe):
    try:
        logger.info("Adding recipe: %s", recipe.name)
        recipe_id = recipe_data.add_recipe(recipe)
        if recipe.ingredients:
            for ingredient in recipe.ingredients:
                ingredient.recipe_id = recipe_id
                ingredient.id = ingredient_data.add_ingredient(ingredient)
        return recipe
            
    except Exception as e:
        logger.error("Unable to add recipe: error: " + str(e))
        return {"message": "Unable to add recipe: error: " + str(e)}


@router.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe: Recipe):
    try:
        updated_recipe = recipe_data.update_recipe(recipe_id, recipe)
        return updated_recipe
    except Exception as e:
        return {"message": "Unable to update recipe: error: " + str(e)}


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    try:
        recipe_data.delete_recipe(recipe_id)
        return {"message": f"Recipe'{recipe_id}' deleted successfully"}
    except Exception as e:
        return {"message": "Unable to delete recipe: error: " + str(e)} 
