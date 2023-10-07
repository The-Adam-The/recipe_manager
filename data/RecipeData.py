import sqlite3
from models.Recipe import Recipe

class RecipeData:
    
    def __init__(self, logger):

        self._logger = logger
        self.create_recipes_table()

    def create_recipes_table(self):
        self._logger.info("Creating recipes table")
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS recipes;")
        con.execute("CREATE TABLE IF NOT EXISTS recipes(recipe_id integer PRIMARY KEY, name text NOT NULL, tags text NOT NULL, time_two integer,  time_four integer, date_created text NOT NULL, last_used text);")
        con.commit()
    
    def drop_recipes_table(self):
        self._logger.info("Dropping recipes table")
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS recipes;")
        con.commit()

    def get_all_recipes(self):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM recipes;")
        all_recipes = cur.fetchall()

        output_recipes = []

        for recipe in all_recipes:
            recipe_dict = {"id": recipe[0], "name":recipe[1], "category":recipe[2], "time":{"two": recipe[3], "four": recipe[4]}, "date_created":recipe[5], "last_used":recipe[6]}
            output_recipes.append(recipe_dict)
        return output_recipes
    
    def get_recipe_by_id(self, id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM recipes WHERE recipe_id = ?;", (id,))
        return cur.fetchone()

    def add_recipe(self, recipe):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("INSERT INTO recipes VALUES (?, ?, ?, ?, ?, ?, ?);", (None, recipe.name, recipe.category, recipe.time["two"], recipe.time["four"], recipe.date_created, recipe.last_used))
        con.commit()
        return cur.lastrowid
    
    
    def update_recipe(self, id, recipe):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        if recipe is type(Recipe):
            self._logger.debug("type is Recipe()")
            cur.execute("UPDATE recipes SET name = ?, tags = ?, time_two = ?, time_four = ?, last_used = ? WHERE recipe_id = ?;", (recipe.name, recipe.category, recipe.time["two"], recipe.time["four"], recipe.last_used, id))
        elif recipe is type(dict):
            self._logger.debug("type is dict")
            cur.execute("UPDATE recipes SET name = ?, tags = ?, time_two = ?, time_four = ?, last_used = ? WHERE recipe_id = ?;", (recipe["name"], recipe["category"], recipe["time"]["two"], recipe["time"]["four"], recipe["last_used"], id))

        # cur.execute("UPDATE recipes SET name = ?, tags = ?, time_two = ?, time_four = ?, last_used = ? WHERE recipe_id = ?;", (recipe.name, recipe.category, recipe.time["two"], recipe.time["four"], recipe.last_used, id))
        con.commit()
        return recipe
    
    def delete_recipe(self, id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("DELETE FROM recipes WHERE recipe_id = ?;", (id,))
        con.commit()
        return id