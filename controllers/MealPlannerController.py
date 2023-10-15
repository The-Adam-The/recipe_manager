import random
from fastapi import APIRouter, Depends
from database import engine, SessionLocal
from data import IngredientData
from data import RecipeData
from schemas import RecipeSchema
from schemas import IngredientSchema
from logging import getLogger

logger = getLogger("recipe-logger")

router = APIRouter()

# Meal Planner + Shopping list generator
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/mealplanner/{num_meals}")
async def meal_planner(num_meals: int, db: SessionLocal = Depends(get_db)):
    try:
        logger.info("Meal planner called. Num meals requested: %s", num_meals)
        recipes: list[RecipeSchema.Recipe] = RecipeData.get_recipes(db)
        logger.debug("Number of recipes pulled from db: %s", len(recipes))
        unused_recipes = []
        used_recipes = []
        ingredients_list = {}
        output_recipes = []

        for recipe in recipes:
            recipe.ingredients: list[IngredientSchema.Ingredient] = IngredientData.get_ingredients_by_recipe_id(db, recipe.id)
            if recipe.last_used == "" or recipe.last_used == None:
                unused_recipes.append(recipe)
                random.shuffle(unused_recipes)
            else: 
                used_recipes.append(recipe)
                random.shuffle(used_recipes)

        num_unused_recipes = len(unused_recipes)
        logger.debug("Number of unused recipes: %s", num_unused_recipes)
        logger.debug("Number of used recipes: %s", len(used_recipes))
        if num_unused_recipes > 0:
            if num_unused_recipes >= int(num_meals):
                logger.debug("More unused recipes(%s) than requested meals(%s), using (%s)unused recipes", num_unused_recipes, int(num_meals), num_unused_recipes)
                selected_recipes = unused_recipes[:int(num_meals)]
            elif num_unused_recipes < int(num_meals):
                logger.debug("Less unused recipes(%s) than requested meals(%s), using all unused recipes and filling in with used recipes", num_unused_recipes, int(num_meals))
                selected_recipes = unused_recipes
                selected_recipes.extend(used_recipes[:int(num_meals)-num_unused_recipes])
        else:
            logger.debug("No unused recipes found, using all recipes")
            selected_recipes = used_recipes[:int(num_meals)]

        try:
            for selected_recipe in selected_recipes:
                logger.debug("Updating db with last_used date for recipe: %s", selected_recipe.name)
                # logger.debug("Selected recipe: %s", selected_recipe)
                RecipeData.update_recipe(db, selected_recipe.id, selected_recipe)
                # logger.debug("Adding recipe: %s", selected_recipe["name"])
                for ingredient in selected_recipe.ingredients:
                    logger.debug("Adding ingredient: %s", ingredient.name)
                    if ingredients_list.get(ingredient.name, None) is None: 
                        logger.debug("Ingredient %s, not in ingredients_list, adding values: %s", ingredient.name, ingredient)
                        ingredients_list[ingredient.name] = {"quantities": [ingredient.quantity], "unit": ingredient.unit, "perishable": ingredient.perishable, "recipes": [selected_recipe.name], "recipe_id": [selected_recipe.id]}
                    else:
                        logger.debug("Ingredient already in output_recipes, adding %s quantities", ingredient.name)
                        ingredients_list[ingredient.name]["quantities"].append(ingredient.quantity)
                        ingredients_list[ingredient.name]["recipes"].append(selected_recipe.name)
                        ingredients_list[ingredient.name]["recipe_id"].append(selected_recipe.id)
        
            for key, value in ingredients_list.items():
                sum_value = int(sum(value["quantities"])) if is_integer(value["quantities"][0]) and 1 <= int(sum(value["quantities"])) else float(value["quantities"][0])
                ingredients_list[key]["total_quantity"] = sum_value

        except Exception as e:
            logger.error("Error consolidating ingredients: %s", e)
            return e

        return ingredients_list

    except Exception as e:
        return {"message": "Unable to get recipes: error: " + str(e)}
