from typing import Union
from fastapi import FastAPI, Request
import data.RecipeData as RecipeData
import data.IngredientData as IngredientData
from models.Recipe import Recipe
from models.Ingredient import Ingredient
from pprint import pprint
from json import JSONDecodeError


#uvicorn controllers.RecipeController:app --reload

app = FastAPI()
recipe_data = RecipeData.RecipeData()
ingredient_data = IngredientData.IngredientData()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/recipes")
def read_recipes():
    return recipe_data.get_all_recipes()

@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int):

    recipe = recipe_data.get_recipe_by_id(recipe_id)
    print("recipe: ", recipe)
    return recipe

@app.post("/recipes")
async def add_recipe(recipe: Recipe):
    recipe_id = recipe_data.add_recipe(recipe)
    return recipe_id


@app.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe: Recipe):
    print(recipe_id, recipe)
    updated_recipe = recipe_data.update_recipe(recipe_id, recipe)
    return updated_recipe

@app.delete("/recipes/{recipe_id}")
async def delele_recipe(recipe_id: int):
    recipe_data.delete_recipe(recipe_id)
    return {"message": f"Recipe'{recipe_id}' deleted successfully"}


@app.post("/createrecipetable")
def create_recipes_table():
    recipe_data.create_recipes_table()
    return {"message": "Recipes table created successfully"}


@app.delete("/droprecipes")
def drop_recipes():
    recipe_data.drop_recipes_table()
    return {"message": "Recipes table dropped successfully"}


@app.get("/ingredients")
async def read_ingredients():
    return ingredient_data.get_all_ingredients()


@app.post("/ingredients")
async def add_ingredient(ingredients: Ingredient | list[Ingredient]):

    if isinstance(ingredients, list):
        output = []
        for ingredient in ingredients:
            ingredient.id = ingredient_data.add_ingredient(ingredient)
            output.append(ingredient)
        return output
    elif isinstance(ingredients, Ingredient):
        ingredients.id = ingredient_data.add_ingredient(ingredients)
        return ingredients
    else: 
        return "Invalid input, try again."


@app.put("/ingredients/{ingredient_id}")
async def update_ingredient(ingredient_id: int, ingredient: Ingredient):
    updated_ingredient = ingredient_data.update_ingredient(ingredient_id, ingredient)
    return updated_ingredient


@app.delete("/ingredients/{ingredient_id}")
async def delele_ingredient(ingredient_id: int):
    ingredient_data.delete_ingredient(ingredient_id)
    return {"message": f"Ingredient'{ingredient_id}' deleted successfully"}


@app.post("/createingredientstable")
async def create_ingredients_table():
    ingredient_data.create_ingredients_table()
    return {"message": "Ingredients table created successfully"}

@app.delete("/dropingredients")
async def drop_ingredients():
    ingredient_data.drop_ingredients_table()
    return {"message": "Ingredients table dropped successfully"}