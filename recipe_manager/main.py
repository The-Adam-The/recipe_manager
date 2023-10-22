import uvicorn
from fastapi import FastAPI
from controllers import (RecipeController, IngredientController, GroceryListController)
from logging.config import dictConfig
from config.LogConfig import log_config
from logging import getLogger


dictConfig(log_config)
logger = getLogger("recipe-logger")

app = FastAPI(debug=True)

app.include_router(RecipeController.router)
app.include_router(IngredientController.router)
app.include_router(GroceryListController.router)


@app.get("/")
def read_root():
    return {"message": "RecipeManager API welcomes you!"}

#uvicorn controllers.RecipeController:app --reload
if __name__ == "__main__":
    logger.info("Starting RecipeManager API")
    uvicorn.run(app)