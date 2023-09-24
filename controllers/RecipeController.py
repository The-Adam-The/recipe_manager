from typing import Union
from fastapi import FastAPI, Request
import data.RecipeData as RecipeData
import data.IngredientData as IngredientData
from models.Recipe import Recipe
from models.Ingredient import Ingredient
from pprint import pprint
from json import JSONDecodeError

#TODO: Add logging
#uvicorn controllers.RecipeController:app --reload

app = FastAPI()
recipe_data = RecipeData.RecipeData()
ingredient_data = IngredientData.IngredientData()


@app.get("/")
def read_root():
    return {"message": "RecipeManager API welcomes you!"}

@app.get("/recipes")
def read_recipes():
    try:
        recipes: list[dict] = recipe_data.get_all_recipes()
        for recipe in recipes:
            recipe["ingredients"] = ingredient_data.get_ingredients_by_recipe_id(recipe["id"])
        print("recipes: ", recipes)
        return recipes
    except Exception as e:
        return {"message": "Unable to get recipes: error: " + str(e)}

@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int):
    try:
        recipe = recipe_data.get_recipe_by_id(recipe_id)
        recipe["ingredients"] = ingredient_data.get_ingredients_by_recipe_id(recipe_id)
        return recipe
    except Exception as e:
        return {"message": "Unable to get recipe: error: " + str(e)}
    

@app.post("/recipes")
async def add_recipe(recipe: Recipe):
    try:
        print(recipe)
        recipe_id = recipe_data.add_recipe(recipe)
        if recipe.ingredients:
            for ingredient in recipe.ingredients:
                ingredient.recipe_id = recipe_id
                ingredient.id = ingredient_data.add_ingredient(ingredient)
        return recipe
             
    except Exception as e:
        print("Unable to add recipe: error: " + str(e))
        return {"message": "Unable to add recipe: error: " + str(e)}


@app.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe: Recipe):
    try:
        updated_recipe = recipe_data.update_recipe(recipe_id, recipe)
        return updated_recipe
    except Exception as e:
        return {"message": "Unable to update recipe: error: " + str(e)}
    
@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    try:
        recipe_data.delete_recipe(recipe_id)
        return {"message": f"Recipe'{recipe_id}' deleted successfully"}
    except Exception as e:
        return {"message": "Unable to delete recipe: error: " + str(e)} 

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

@app.get("/ingredients/{ingredient_id}")
async def read_ingredient(ingredient_id: int):
    return ingredient_data.get_ingredient_by_id(ingredient_id)


@app.post("/ingredients")
async def add_ingredient(ingredients: Ingredient | list[Ingredient]):
    try:
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
    except Exception as e:
        return {"message": "Unable to add ingredient: error: " + str(e)}


@app.put("/ingredients/{ingredient_id}")
async def update_ingredient(ingredient_id: int, ingredient: Ingredient):
    try:
        updated_ingredient = ingredient_data.update_ingredient(ingredient_id, ingredient)
        return updated_ingredient
    except Exception as e:
        return {"message": "Unable to update ingredient: error: " + str(e)}

@app.delete("/ingredients/{ingredient_id}")
async def delele_ingredient(ingredient_id: int):
    try:
        ingredient_data.delete_ingredient(ingredient_id)
        return {"message": f"Ingredient'{ingredient_id}' deleted successfully"}
    except Exception as e:
        return {"message": "Unable to delete ingredient: error: " + str(e)}








# Db management functions
@app.post("/createingredientstable")
async def create_ingredients_table():
    ingredient_data.create_ingredients_table()
    return {"message": "Ingredients table created successfully"}

@app.delete("/dropingredients")
async def drop_ingredients():
    ingredient_data.drop_ingredients_table()
    return {"message": "Ingredients table dropped successfully"}