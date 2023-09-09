import os
import time
import json
import pathlib


def show_recipe_details(recipe, nonperishables, perishables, current_ingredient):
    os.system('cls')
    if recipe["name"]:
        print("")
        print(recipe["name"])
        print("")
    if recipe["category"]:
        print("******************************")
        print("")
    if recipe["id"]:
        print("Recipe Card Number: ", 0)
    if recipe["category"]:
        print("    Category: " + recipe["category"])
        print("")
    if recipe["time"]["two"]:
        print("    Time for 2 People(minutes): " + recipe["time"]["two"])
    if recipe["time"]["four"]:
        print("    Time for 4 People(minutes): " + recipe["time"]["four"])
    
    if nonperishables or perishables:
        print("")
        print("    Ingredients:")
    if nonperishables:
        print("")
        print("        Nonperishable:")
        for ingredient in nonperishables:
            print("           - " + ingredient["name"] + " " + ingredient["quantity"] + ingredient["unit"])              
    if perishables:
        print("")
        print("        Perishable:")
        for ingredient in perishables:
            print("          - " + ingredient["name"] + " " + ingredient["quantity"] +  ingredient["unit"])
    if recipe["category"]:
        print("")
        print("******************************")
    print("")
    print("")

    if current_ingredient:
        print("")
        print("    Current Ingredient: " + current_ingredient)
        print("")
        print("")


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def time_input_check(num_people: int, recipe, nonperishables, perishables, current_ingredient):
    while True:
        print("Enter (Q) to quit")
        time_input = input(f"Enter Time for {num_people} People(minutes): ")
        if time_input == "Q":
            exit(1)
        elif is_integer(time_input):
            return time_input
        else: 
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            print(f"Invalid Input '{time_input}'. Needs to be int. Please try again.")
            print("")

def ingredient_quanitity_check(ingredient, recipe, nonperishables, perishables, current_ingredient):
    while True:
        print("Enter (Q) to quit")
        ingredient_quantity = input("Enter Ingredient Quantity: ")
        if ingredient_quantity == "Q":
            exit(1)
        elif is_integer(ingredient_quantity) or is_float(ingredient_quantity):
            ingredient["quantity"] = str(ingredient_quantity)
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            return
        else:
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            print(f"Invalid Input '{ingredient_quantity}'. Needs to be float or int. Please try again.")

def ingredient_unit_check(ingredient, recipe, nonperishables, perishables, current_ingredient):
    while True:
        print("Enter (Q) to quit")
        ingredient_unit = input("Enter Ingredient Unit: ").lower().strip()
        if ingredient_unit == "Q":
            exit(1)
        elif ingredient_unit == "ml" or ingredient_unit == "g" or ingredient_unit == "tsp" or ingredient_unit == "tbsp" or ingredient_unit == "unit":
            ingredient["unit"] = str(ingredient_unit)
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            return
        else:
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            print(f"Invalid Input '{ingredient_unit}'. Needs to be 'ml', 'g', 'tsp', 'tbsp', or 'unit'. Please try again.")


def enter_ingredient(ingredient_type: str, recipe, nonperishables, perishables, current_ingredient):
    
    enter_ingredients = True
    while enter_ingredients:
        
        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
        enter_ingredient = True
        print(f"Enter {ingredient_type} Ingredients:")
        
        while enter_ingredient:
        
            ingredient = {"name": "", "quantity": "", "unit": ""}
            
            ingredient["name"] = input("Enter Ingredient Name: ") 
            current_ingredient = ingredient["name"]
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            
            ingredient_quanitity_check(ingredient, recipe, nonperishables, perishables, current_ingredient)
            current_ingredient = ingredient["name"] + " " + ingredient["quantity"]
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            

            ingredient_unit_check(ingredient, recipe, nonperishables, perishables, current_ingredient)
            current_ingredient += ingredient["unit"]
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            

            ingredient_confirmation = input("Is this the correct? (y/n)")
            if ingredient_confirmation == "Q":
                exit(1)
            elif ingredient_confirmation == "y":
                current_ingredient = ""
                if ingredient_type == "Nonperishable":
                    nonperishables.append(ingredient)
                elif ingredient_type == "Perishable":
                    perishables.append(ingredient)
                else:
                    print("Invalid ingredient type")
                show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                enter_ingredient = False
                return
            
            elif ingredient_confirmation == "n":
                show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                amend_ingredient = True
                while amend_ingredient:
                    print("Amend which value?")
                    print("    1. Name")                                
                    print("    2. Quantity")
                    print("    3. Unit")
                    print("    4. Done")
                    print("    Q. Quit")
                    amend_value = input()
                    if amend_value == "1":
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                        ingredient["name"] = input("Enter new name: ") 
                        current_ingredient = ingredient["name"] + " " + ingredient["quantity"] + ingredient["unit"]
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                    
                    elif amend_value == "2":
                        ingredient_quanitity_check(ingredient, recipe, nonperishables, perishables, current_ingredient)
                        current_ingredient = ingredient["name"] + " " + ingredient["quantity"] + ingredient["unit"]
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                    
                    elif amend_value == "3":
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                        ingredient["unit"] =  input("Enter new unit: ")
                        current_ingredient = ingredient["name"] + " " + ingredient["quantity"] + ingredient["unit"]
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                    
                    elif amend_value == "4":
                        amend_ingredient = False
                        if ingredient_type == "Nonperishable":
                            nonperishables.append(ingredient)
                        elif ingredient_type == "Perishable":
                            perishables.append(ingredient)
                        else: 
                            print("Invalid ingredient type")
                        current_ingredient = ""
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                    elif amend_value == "Q":
                        exit(1)
            else:
                print("Invalid Input, please try again.")

def add_recipe_manager():
    os.system('cls')
    nonperishables: list = []
    perishables: list = []
    recipe = {"name": "", "id": None, "time": {"two":0, "four": 0 }, "category": "", "nonperishables": [], "perishables": []}
    current_ingredient = ""
    
    recipe["name"] = input("Enter Recipe Name: ")
    show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
    
    recipe["category"] = input("Enter Recipe Category: ")
    show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
    
    recipe["time"]["two"] = time_input_check(2, recipe, nonperishables, perishables, current_ingredient)
    show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
    
    recipe["time"]["four"] = time_input_check(4, recipe, nonperishables, perishables, current_ingredient)
    show_recipe_details(recipe, nonperishables, perishables, current_ingredient) 

    enter_recipe = True
    while enter_recipe:

        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
        print("1. Add Perishable Ingredients")
        print("2. Add Nonperishable Ingredients")
        print("3. Save Recipe")
        print("4. Return to Main Menu")
        print("Q. Quit")

        option = input()
        if option == "4":
            enter_recipe = False
            print("Returning to Main Menu...")
            time.sleep(2)
            return

        elif option == "1":
            enter_perishables = True
            while enter_perishables:
                show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                enter_ingredient("Perishable", recipe, nonperishables, perishables, current_ingredient)
                option = input(f"Would you like to add another perishable ingredient? (y/n)")
                
                if option == "n":
                    recipe["perishables"] = perishables
                    enter_perishables = False
                else:
                    continue
        elif option == "2":
            enter_nonperishables = True
            while enter_nonperishables:
                show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                enter_ingredient("Nonperishable", recipe, nonperishables, perishables, current_ingredient)
                option = input(f"Would you like to add another Nonperishable ingredient? (y/n)")
                if option == "n":
                    recipe["Nonperishables"] = nonperishables
                    enter_nonperishables = False
                elif option == "y":
                    continue
                else:
                    print("Invalid Input, please try again.")

        elif option == "3":
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            if not pathlib.Path('recipes.json').exists():
                print("Creating new file 'recipes.json'...")
                recipe["id"] = 0
                with open('recipes.json', 'w') as f:
                    json.dump(recipe, f)
            else:
                print("Appending to new recipes to 'recipes.json'...")
                with open('recipes.json', 'r') as f:
                    recipes = json.load(f)                        
                    recipe["id"] = len(recipes["recipes"])

                with open('recipes.json', 'w') as f:
                    recipes["recipes"].append(recipe)
                    json.dump(recipes, f)

            print("Recipe saved!")
            time.sleep(2)
            enter_recipe = False
            os.system('cls')

        elif option == "Q":
            exit(1)
        print("Enter perishable Ingredients:")