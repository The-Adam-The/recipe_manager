from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_used = Column(String)
    date_created = Column(String)
    category = Column(String)
    time_two = Column(Integer)
    time_four = Column(Integer)


class Ingredient(Base):
    __tablename__ = "Ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    unit = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    perishable = Column(Boolean, default=False)
