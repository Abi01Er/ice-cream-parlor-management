
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, engine, Base 
from models import (
    Flavor, 
    Ingredient, 
    Allergen, 
    FlavorIngredient, 
    FlavorAllergen, 
    Cart
)



class IceCreamParlor:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()
    
    def add_flavor(self, name, description, is_seasonal, price, stock_quantity):
        try:
            flavor = Flavor(
                name=name, 
                description=description, 
                is_seasonal=is_seasonal, 
                price=price, 
                stock_quantity=stock_quantity
            )
            self.session.add(flavor)
            self.session.commit()
            return flavor
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding flavor: {e}")
            return None
    
    def add_ingredient(self, name, stock_quantity, unit):
        try:
            ingredient = Ingredient(
                name=name, 
                stock_quantity=stock_quantity, 
                unit=unit
            )
            self.session.add(ingredient)
            self.session.commit()
            return ingredient
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding ingredient: {e}")
            return None
    
    def add_allergen(self, name):
        try:
            allergen = Allergen(name=name)
            self.session.add(allergen)
            self.session.commit()
            return allergen
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding allergen: {e}")
            return None
    
    def add_ingredient_to_flavor(self, flavor_name, ingredient_name):
        try:
            flavor = self.session.query(Flavor).filter_by(name=flavor_name).first()
            ingredient = self.session.query(Ingredient).filter_by(name=ingredient_name).first()
            
            if flavor and ingredient:
                flavor_ingredient = FlavorIngredient(
                    flavor_id=flavor.id, 
                    ingredient_id=ingredient.id
                )
                self.session.add(flavor_ingredient)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding ingredient to flavor: {e}")
            return False
    
    def add_allergen_to_flavor(self, flavor_name, allergen_name):
        try:
            flavor = self.session.query(Flavor).filter_by(name=flavor_name).first()
            allergen = self.session.query(Allergen).filter_by(name=allergen_name).first()
            
            if flavor and allergen:
                flavor_allergen = FlavorAllergen(
                    flavor_id=flavor.id, 
                    allergen_id=allergen.id
                )
                self.session.add(flavor_allergen)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding allergen to flavor: {e}")
            return False
    
    def search_flavors(self, name=None, is_seasonal=None):
        query = self.session.query(Flavor)
        if name:
            query = query.filter(Flavor.name.ilike(f'%{name}%'))
        if is_seasonal is not None:
            query = query.filter(Flavor.is_seasonal == is_seasonal)
        return query.all()
    
    def add_to_cart(self, flavor_name, quantity=1):
        try:
            flavor = self.session.query(Flavor).filter_by(name=flavor_name).first()
            
            if flavor and flavor.stock_quantity >= quantity:
                cart_item = Cart(flavor_id=flavor.id, quantity=quantity)
                flavor.stock_quantity -= quantity
                self.session.add(cart_item)
                self.session.commit()
                return cart_item
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding to cart: {e}")
            return None
    
    def view_cart(self):
        cart_items = self.session.query(Cart).all()
        return [(item.flavor.name, item.quantity, item.flavor.price * item.quantity) for item in cart_items]
    
    def clear_cart(self):
        try:
            self.session.query(Cart).delete()
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error clearing cart: {e}")
            return False
