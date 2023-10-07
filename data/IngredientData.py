import sqlite3
from models.Ingredient import Ingredient

class IngredientData:

    def __init__(self, logger):
        self._logger = logger
        self.create_ingredients_table()

    def create_ingredients_table(self):
        self._logger.info("Creating ingredients table")
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS ingredients;")
        con.execute("CREATE TABLE IF NOT EXISTS ingredients(ingredient_id INTEGER PRIMARY KEY, name text NOT NULL, quantity real NOT NULL, unit TEXT NOT NULL, recipe_id integer NOT NULL, perishable integer NOT NULL, FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id));")
        con.commit()

    def drop_ingredients_table(self):
        self._logger.info("Dropping ingredients table")
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS ingredients;")
        con.commit()

    def get_all_ingredients(self):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM ingredients;")
        ingredients = cur.fetchall()
        output_ingredients = []
        for ingredient in ingredients:
            ingredient_dict = {"id": ingredient[0], "name":ingredient[1], "quantity":ingredient[2], "unit":ingredient[3], "recipe_id":ingredient[4], "perishable":ingredient[5]}
            output_ingredients.append(ingredient_dict)

        return output_ingredients
    
    def get_ingredient_by_id(self, id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM ingredients WHERE ingredient_id = ?;", (id,))
        ingredient = cur.fetchone()
        ingredient_dict = {"id": ingredient[0], "name":ingredient[1], "quantity":ingredient[2], "unit":ingredient[3], "recipe_id":ingredient[4], "perishable":ingredient[5]}
        return ingredient_dict

    def add_ingredient(self, ingredient: Ingredient):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("INSERT INTO ingredients VALUES (?, ?, ?, ?, ?, ?);", (None, ingredient.name, ingredient.quantity, ingredient.unit, ingredient.recipe_id, ingredient.perishable))
        con.commit()
        return cur.lastrowid
    
    def update_ingredient(self, id, ingredient):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("UPDATE ingredients SET name = ?, quantity = ?, unit = ?, recipe_id = ?, perishable = ? WHERE ingredient_id = ?;", (ingredient.name, ingredient.quantity, ingredient.unit, ingredient.recipe_id, ingredient.perishable, id))
        con.commit()
        return ingredient
    
    def delete_ingredient(self, id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("DELETE FROM ingredients WHERE ingredient_id = ?;", (id,))
        con.commit()
        return id
    
    def get_ingredients_by_recipe_id(self, recipe_id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM ingredients WHERE recipe_id = ?;", (recipe_id,))
        ingredients = cur.fetchall()
        output_ingredients = []
        for ingredient in ingredients:
            ingredient_dict = {"id": ingredient[0], "name":ingredient[1], "quantity":ingredient[2], "unit":ingredient[3], "recipe_id":ingredient[4], "perishable":ingredient[5]}
            output_ingredients.append(ingredient_dict)
        return output_ingredients