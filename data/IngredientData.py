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

# def update_ingredient(self, id, ingredient):
#     con = sqlite3.connect("recipes.db")
#     cur = con.cursor()
#     cur.execute("UPDATE ingredients SET name = ?, quantity = ?, unit = ?, recipe_id = ?, perishable = ? WHERE ingredient_id = ?;", (ingredient.name, ingredient.quantity, ingredient.unit, ingredient.recipe_id, ingredient.perishable, id))
#     con.commit()
#     return ingredient

# def delete_ingredient(self, id):
#     con = sqlite3.connect("recipes.db")
#     cur = con.cursor()
#     cur.execute("DELETE FROM ingredients WHERE ingredient_id = ?;", (id,))
#     con.commit()
#     return id

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