from fastapi import APIRouter
from data.IngredientData import IngredientData
from models.Ingredient import Ingredient
from logging import getLogger

logger = getLogger("recipe-logger")
logger.info("Creating IngredientController")
ingredient_data = IngredientData(logger)
router = APIRouter()

@router.get("/ingredients")
async def read_ingredients():
    return ingredient_data.get_all_ingredients()

@router.get("/ingredients/{ingredient_id}")
async def read_ingredient(ingredient_id: int):
    return ingredient_data.get_ingredient_by_id(ingredient_id)


@router.post("/ingredients")
async def add_ingredient(ingredients: Ingredient | list[Ingredient]):
    try:
        if isinstance(ingredients, list):
            output = []
            for ingredient in ingredients:
                ingredient.id = ingredient_data.add_ingredient(ingredient)
                output.routerend(ingredient)
            return output
        elif isinstance(ingredients, Ingredient):
            ingredients.id = ingredient_data.add_ingredient(ingredients)
            return ingredients
        else: 
            return "Invalid input, try again."
    except Exception as e:
        return {"message": "Unable to add ingredient: error: " + str(e)}


@router.put("/ingredients/{ingredient_id}")
async def update_ingredient(ingredient_id: int, ingredient: Ingredient):
    try:
        updated_ingredient = ingredient_data.update_ingredient(ingredient_id, ingredient)
        return updated_ingredient
    except Exception as e:
        return {"message": "Unable to update ingredient: error: " + str(e)}

@router.delete("/ingredients/{ingredient_id}")
async def delete_ingredient(ingredient_id: int):
    try:
        ingredient_data.delete_ingredient(ingredient_id)
        return {"message": f"Ingredient'{ingredient_id}' deleted successfully"}
    except Exception as e:
        return {"message": "Unable to delete ingredient: error: " + str(e)}