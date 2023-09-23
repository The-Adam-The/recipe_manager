import json
import time
from pprint import pprint
from random import randint
import os
from RecipeManager import is_integer
import pathlib

def load_recipes():
    with open('recipes.json') as f:
        recipes = json.load(f)
    return recipes


def create_shopping_list(consolidate_dict):
    date = time.strftime("%Y-%m-%d")
    shopping_list = "Shopping list for week commencing " + date
    shopping_list += "\n\n" + "Recipes: " + "\n"
    for recipe in consolidate_dict["recipes"]:
        shopping_list += "\n" + "    -" + recipe + "\n"
    shopping_list += "\n\n" + "Perishables: " + "\n"
    for key, value in consolidate_dict["perishables"].items():
        if not value["unit"] == "u":
            shopping_list += "\n" + "    -" + key + " " + str(value["total_quantity"]) + value["unit"] + "\n"
        else:
            shopping_list += "\n" + "    -" + key + " " + str(value["total_quantity"]) + "\n"
    
    shopping_list += "\n" + "Nonperishables: " + "\n"
    for key, value in consolidate_dict["nonperishables"].items():
        if not value["unit"] == "u":
            shopping_list += "\n" + "    -" + key + " " + str(value["total_quantity"]) + value["unit"] + "\n"
        else:
            shopping_list += "\n" + "    -" + key + " " + str(value["total_quantity"]) + "\n"

    if not pathlib.Path("./shopping_lists").exists():
        os.mkdir("./shopping_lists")

    if not pathlib.Path("./shopping_lists/shopping_list_" + date + ".txt").exists():
        with open("./shopping_lists/shopping_list_" + date + ".txt", "x") as f: 
            f.write(shopping_list)
    else:
        with open("./shopping_lists/shopping_list_" + date + ".txt", "w") as f: 
            f.write(shopping_list)
             

def menu_generator(num_days=5):
    os.system('cls') 
    recipes = load_recipes()
    
    total_num_recipes = len(recipes["recipes"])


    selected_recipes = []
    selected_indexes = []

    while len(selected_recipes) < num_days:
        rand_index = randint(0, total_num_recipes-1)
        if not rand_index in selected_indexes:
            selected_indexes.append(rand_index) 
            selected_recipes.append(recipes["recipes"][rand_index])
        else:
            continue
    
    consolidate_dict = {
        "recipes": [],
        "perishables": {},
        "nonperishables": {}
    }

    for selected_recipe in selected_recipes:
        consolidate_dict["recipes"].append(selected_recipe["name"])
        for perishable_ingredient in selected_recipe["perishables"]:
            if consolidate_dict["perishables"].get(perishable_ingredient["name"], None) is None: 
                consolidate_dict["perishables"][perishable_ingredient["name"]] = {"quantities": [perishable_ingredient["quantity"]], "unit": perishable_ingredient["unit"], "recipes": [selected_recipe["name"]]}
            else:
                consolidate_dict["perishables"][perishable_ingredient["name"]]["quantities"].append(perishable_ingredient["quantity"])
        
        for nonperishable_ingredient in selected_recipe["nonperishables"]:
            if consolidate_dict["nonperishables"].get(nonperishable_ingredient["name"], None) is None: 
                consolidate_dict["nonperishables"][nonperishable_ingredient["name"]] = {"quantities": [nonperishable_ingredient["quantity"]], "unit": nonperishable_ingredient["unit"], "recipes": selected_recipe["name"]}
            else:
                consolidate_dict["nonperishables"][nonperishable_ingredient["name"]]["quantities"].append(nonperishable_ingredient["quantity"])
    
    for key, value in consolidate_dict["nonperishables"].items():
        sum_value = int(sum(value["quantities"])) if is_integer(value["quantities"][0]) and 1 <= int(sum(value["quantities"])) else float(value["quantities"][0])
        consolidate_dict["nonperishables"][key]["total_quantity"] = sum_value
    
    for key, value in consolidate_dict["perishables"].items():        
        sum_value = int(sum(value["quantities"])) if is_integer(value["quantities"][0]) and 1 <= int(sum(value["quantities"])) else float(value["quantities"][0])
        consolidate_dict["perishables"][key]["total_quantity"] = sum_value

    print(consolidate_dict)
    input() 
    create_shopping_list(consolidate_dict)





