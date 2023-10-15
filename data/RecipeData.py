from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from schemas import RecipeSchema as schemas
from models import Recipe
from logging import getLogger

logger = getLogger("recipe-logger")

def create_table(db: Session):
    logger.debug("Creating recipes table")
    db.execute(text("CREATE TABLE IF NOT EXISTS recipes(id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, time_two INTEGER,  time_four INTEGER, date_created TEXT NOT NULL, last_used TEXT);"))
    db.commit()

def drop_table(db: Session):
    logger.debug("Dropping recipes table")
    db.execute(text("DROP TABLE IF EXISTS recipes;"))
    db.commit()


def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    logger.debug("Getting recipes")
    return db.query(Recipe).offset(skip).limit(limit).all()


def get_recipe_by_id(db: Session, id: int):
    logger.debug("Getting recipe by id: %s", id)
    return db.query(Recipe).filter(Recipe.id == id).first()


def add_recipe(db: Session, recipe: schemas.RecipeCreate):
    logger.debug("Adding recipe: %s", recipe)
    db_recipe = Recipe(name=recipe.name, category=recipe.category, time_two=recipe.time_two, time_four=recipe.time_four, date_created=recipe.date_created, last_used=recipe.last_used)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def update_recipe(db: Session, recipe_id: int, recipe: schemas.Recipe):
    logger.debug("Updating recipe: %s", recipe)
    db_query = db.query(Recipe).filter(Recipe.id == recipe_id)
    recipe_to_update = db_query.first()

    recipe_to_update.name = recipe.name
    recipe_to_update.category = recipe.category
    recipe_to_update.time_two = recipe.time_two
    recipe_to_update.time_four = recipe.time_four
    recipe_to_update.date_created = recipe.date_created
    recipe_to_update.last_used = recipe.last_used

    db.add(recipe_to_update)
    db.commit()
    return recipe


def delete_recipe(db: Session, id: int):
    logger.debug("Deleting recipe with id: %s", id)
    db_query = db.query(Recipe).filter(Recipe.id == id)
    recipe_to_delete = db_query.first()
    db.delete(recipe_to_delete)
    db.commit()
    return True

# def create_recipes_table(self):
#     self._logger.info("Creating recipes table")
#     con = sqlite3.connect("recipes.db")
#     con.execute("DROP TABLE IF EXISTS recipes;")
#     con.execute("CREATE TABLE IF NOT EXISTS recipes(recipe_id integer PRIMARY KEY, name text NOT NULL, tags text NOT NULL, time_two integer,  time_four integer, date_created text NOT NULL, last_used text);")
#     con.commit()

