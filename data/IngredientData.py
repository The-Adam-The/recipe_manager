from sqlalchemy.orm import Session
from data import IngredientData as data
from sqlalchemy.sql import text
from schemas import IngredientSchema as schemas
from models import Ingredient
from logging import getLogger

logger = getLogger("recipe-logger")


def create_table(db: Session):
    db.execute(text("CREATE TABLE IF NOT EXISTS ingredients(id INTEGER PRIMARY KEY, name TEXT NOT NULL, quantity REAL NOT NULL, unit TEXT NOT NULL, recipe_id INTEGER NOT NULL, perishable INTEGER NOT NULL, FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id));"))
    db.commit()


def drop_table(db: Session):
    db.execute(text("DROP TABLE IF EXISTS ingredients;"))
    db.commit()

def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ingredient).offset(skip).limit(limit).all()


def get_ingredient_by_id(db: Session, id: int):
    return db.query(Ingredient).filter(Ingredient.id == id).first()


def add_ingredient(db: Session, added_ingredient: schemas.IngredientCreate):
    logger.debug("Adding ingredient: %s", added_ingredient)
    db_ingredient = Ingredient(name=added_ingredient.name, quantity=added_ingredient.quantity, 
                               unit=added_ingredient.unit, recipe_id=added_ingredient.recipe_id, 
                               perishable=added_ingredient.perishable)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def update_ingredient(db: Session, id: int, ingredient: schemas.Ingredient):
    logger.debug("Updating ingredient: %s", ingredient)
    db_query = db.query(Ingredient).filter(Ingredient.id == id)
    ingredient_to_update = db_query.first()

    ingredient_to_update.name = ingredient.name
    ingredient_to_update.quantity = ingredient.quantity
    ingredient_to_update.unit = ingredient.unit
    ingredient_to_update.recipe_id = ingredient.recipe_id
    ingredient_to_update.perishable = ingredient.perishable

    db.add(ingredient_to_update)
    db.commit()
    return ingredient

def delete_ingredient(db: Session, id: int):
    logger.debug("Deleting ingredient with id: %s", id)
    db_query = db.query(Ingredient).filter(Ingredient.id == id)
    ingredient_to_delete = db_query.first()
    db.delete(ingredient_to_delete)
    db.commit()
    return True

# def get_ingredients_by_recipe_id(self, recipe_id):
#     con = sqlite3.connect("recipes.db")
#     cur = con.cursor()
#     cur.execute("SELECT * FROM ingredients WHERE recipe_id = ?;", (recipe_id,))
#     ingredients = cur.fetchall()
#     output_ingredients = []
#     for ingredient in ingredients:
#         ingredient_dict = {"id": ingredient[0], "name":ingredient[1], "quantity":ingredient[2], "unit":ingredient[3], "recipe_id":ingredient[4], "perishable":ingredient[5]}
#         output_ingredients.append(ingredient_dict)
#     return output_ingredients