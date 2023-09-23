import os
import time
from RecipeManager import add_recipe_manager
from MenuGenerator import menu_generator 

if __name__ == '__main__':
    
    app_running = True
    while app_running:
        os.system('cls')
        print("---------------")
        print("Recipe Manager")
        print("")
        print("    1. Add Recipe")
        print("    2. Generate Weekly Menu")
        print("    Q. Quit")
        print("")
        print("---------------")
        print("Select Option")
        
        option = input()
        
        if option == "1":
            add_recipe_manager()
        elif option == "2":
            menu_generator()
            continue
        elif option == "Q":
            app_running = False
            
            os.system('cls')
            print("Exiting...")
            continue
    exit(0)
