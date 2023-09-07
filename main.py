import json
import os
import pathlib
import time


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


def enter_ingredient(ingredient_type: str, recipe, nonperishables, perishables, current_ingredient):
    
    enter_ingredients = True
    while enter_ingredients:
        
        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
        enter_ingredient = True
        print(f"Enter {ingredient_type} Ingredients:")
        
        while enter_ingredient:
        
            ingredient_name = input("Enter Ingredient Name: ")
            current_ingredient = ingredient_name
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            
            ingredient_quantity = input("Enter Ingredient Quantity: ")
            current_ingredient += " " + ingredient_quantity
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            
            ingredient_unit = input("Enter Ingredient Unit: ")
            current_ingredient += ingredient_unit
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            
            ingredient = {"name": ingredient_name, "quantity": ingredient_quantity, "unit": ingredient_unit}
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
                        show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                        ingredient["quantity"] = input("Enter new quantity: ")
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





if __name__ == '__main__':
    
    app_running = True
    while app_running:
        os.system('cls')
        print("---------------")
        print("Recipe Manager")
        print("")
        print("    1. Add Recipe")
        print("    Q. Quit")
        print("")
        print("---------------")
        print("Select Option")
        
        option = input()
        
        if option == "1":
            os.system('cls')
            nonperishables: list = []
            perishables: list = []
            recipe = {"name": "", "id": None, "time": {"two":0, "four": 0 }, "category": "", "nonperishables": [], "perishables": []}
            current_ingredient = ""
            
            recipe["name"] = input("Enter Recipe Name: ")
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            recipe["category"] = input("Enter Recipe Category: ")
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            recipe["time"]["two"] = input("Enter Time for 2 People(minutes): ")
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
            recipe["time"]["four"] = input("Enter Time for 4 People(minutes): ")
            show_recipe_details(recipe, nonperishables, perishables, current_ingredient) 

            enter_recipe = True
            while enter_recipe:

                show_recipe_details(recipe, nonperishables, perishables, current_ingredient)
                print("1. Add Perishable Ingredients")
                print("2. Add Nonperishable Ingredients")
                print("3. Save Recipe")
                print("Q. Quit")

                option = input()

                if option == "1":
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

        elif option == "Q":
            app_running = False
            
            os.system('cls')
            print("Exiting...")
            continue
    exit(0)
