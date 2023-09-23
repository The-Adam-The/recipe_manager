import sqlite3
from models.Ingredient import Ingredient

class IngredientData:

    def __init__(self):
        self.create_ingredients_table()

    def create_ingredients_table(self):
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS ingredients;")
        con.execute("CREATE TABLE IF NOT EXISTS ingredients(ingredient_id INTEGER PRIMARY KEY, name text NOT NULL, quantity real NOT NULL, unit TEXT NOT NULL, recipe_id integer NOT NULL, perishable integer NOT NULL, FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id));")
        con.commit()

    def drop_ingredients_table(self):
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS ingredients;")
        con.commit()

    def get_all_ingredients(self):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM ingredients;")
        return cur.fetchall()
    
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