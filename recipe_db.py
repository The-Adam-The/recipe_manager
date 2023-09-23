import sqlite3

con = sqlite3.connect('recipes.db')
cur = con.cursor()

cur.execute("CREATE TABLE recipes(id integer NOT NULL, name text NOT NULL, tags text NOT NULL, time_two integer,  time_four integer);")
cur.execute("CREATE TABLE ingredients(id integer NOT NULL, name text NOT NULL, quantity real NOT NULL, unit TEXT NOT NULL, recipe_id integer NOT NULL);")
