import sqlite3

class RecipeData:
    
    def __init__(self):

        self.create_recipes_table()

    def create_recipes_table(self):
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS recipes;")
        con.execute("CREATE TABLE IF NOT EXISTS recipes(recipe_id integer PRIMARY KEY, name text NOT NULL, tags text NOT NULL, time_two integer,  time_four integer, date_created text NOT NULL);")
        con.commit()
    
    def drop_recipes_table(self):
        con = sqlite3.connect("recipes.db")
        con.execute("DROP TABLE IF EXISTS recipes;")
        con.commit()

    def get_all_recipes(self):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM recipes;")
        return cur.fetchall()

    def get_recipe_by_id(self, id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM recipes WHERE recipe_id = ?;", (id,))
        return cur.fetchone()

    # def get_all_recipes_and_ingredients(self):
    #     con = sqlite3.connect("recipes.db")
    #     cur = con.cursor()
    #     cur.execute("""SELECT r.recipe_id,
    #                     r.name, 
    #                     i.name 
    #                     FROM recipes as r;""") 

    def add_recipe(self, recipe):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("INSERT INTO recipes VALUES (?, ?, ?, ?, ?, ?);", (None, recipe.name, recipe.category, recipe.time["two"], recipe.time["four"], recipe.date_created))
        con.commit()
        return cur.lastrowid
    
    
    def update_recipe(self, id, recipe):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("UPDATE recipes SET name = ?, tags = ?, time_two = ?, time_four = ? WHERE recipe_id = ?;", (recipe.name, recipe.category, recipe.time["two"], recipe.time["four"], id))
        con.commit()
        return recipe
    
    def delete_recipe(self, id):
        con = sqlite3.connect("recipes.db")
        cur = con.cursor()
        cur.execute("DELETE FROM recipes WHERE recipe_id = ?;", (id,))
        con.commit()
        return id