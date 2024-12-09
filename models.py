from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 


class Flavor(Base):
    __tablename__ = 'flavors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_seasonal = Column(Boolean, default=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    ingredients = relationship("Ingredient", secondary="flavor_ingredients")
    allergens = relationship("Allergen", secondary="flavor_allergens")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    stock_quantity = Column(Float, default=0)
    unit = Column(String)
    
    flavors = relationship("Flavor", secondary="flavor_ingredients")

class Allergen(Base):
    __tablename__ = 'allergens'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    flavors = relationship("Flavor", secondary="flavor_allergens")

class FlavorIngredient(Base):
    __tablename__ = 'flavor_ingredients'
    
    flavor_id = Column(Integer, ForeignKey('flavors.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)

class FlavorAllergen(Base):
    __tablename__ = 'flavor_allergens'
    
    flavor_id = Column(Integer, ForeignKey('flavors.id'), primary_key=True)
    allergen_id = Column(Integer, ForeignKey('allergens.id'), primary_key=True)

class Cart(Base):
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    flavor_id = Column(Integer, ForeignKey('flavors.id'))
    quantity = Column(Integer, default=1)
    
    flavor = relationship("Flavor")