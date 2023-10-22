import uvicorn
from fastapi import FastAPI
from controllers import (RecipeController, IngredientController, GroceryListController)
from logging.config import dictConfig
from config.LogConfig import log_config
from logging import getLogger
import configparser


dictConfig(log_config)
logger = getLogger("recipe-logger")


config = configparser.ConfigParser()
config.read("recipe_manager/config/config.ini")

app = FastAPI(debug=True)

app.include_router(RecipeController.router)
app.include_router(IngredientController.router)
app.include_router(GroceryListController.router)
development_mode = config.getboolean("DEFAULT", "development_mode")
host_ip = config.get("DEFAULT", "host_ip")
host_port = config.getint("DEFAULT", "host_port")

@app.get("/")
def read_root():
    return {"message": "RecipeManager API welcomes you!"}

#uvicorn controllers.RecipeController:app --reload
if __name__ == "__main__":
    if development_mode:
        logger.info("Starting RecipeManager API in development mode")
        uvicorn.run(app)
    else:
        logger.info("Starting RecipeManager API")
        uvicorn.run(app, host=host_ip, port=host_port)
