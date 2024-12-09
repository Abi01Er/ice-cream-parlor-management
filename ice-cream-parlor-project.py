# Project Structure
# ice_cream_parlor/
#   ├── main.py
#   ├── models.py
#   ├── database.py
#   ├── crud.py
#   ├── requirements.txt
#   ├── Dockerfile
#   └── README.md

# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
engine = create_engine('sqlite:///ice_cream_parlor.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

# models.py
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

# crud.py
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

# main.py
def main():
    parlor = IceCreamParlor()
    
    # Add some initial data
    parlor.add_allergen("Nuts")
    parlor.add_allergen("Dairy")
    
    parlor.add_ingredient("Heavy Cream", 100, "liters")
    parlor.add_ingredient("Sugar", 50, "kg")
    
    chocolate = parlor.add_flavor("Chocolate Delight", "Rich chocolate flavor", True, 5.99, 20)
    parlor.add_ingredient_to_flavor("Chocolate Delight", "Heavy Cream")
    parlor.add_allergen_to_flavor("Chocolate Delight", "Dairy")
    
    # Simple interactive menu (you can enhance this)
    while True:
        print("\n--- Ice Cream Parlor Management ---")
        print("1. Search Flavors")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Clear Cart")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter flavor name (or press enter for all): ")
            seasonal = input("Seasonal? (Y/N, or press enter for all): ")
            
            seasonal_filter = None
            if seasonal.upper() == 'Y':
                seasonal_filter = True
            elif seasonal.upper() == 'N':
                seasonal_filter = False
            
            flavors = parlor.search_flavors(name, seasonal_filter)
            for flavor in flavors:
                print(f"{flavor.name} - ${flavor.price} ({'Seasonal' if flavor.is_seasonal else 'Regular'})")
        
        elif choice == '2':
            flavor_name = input("Enter flavor name to add to cart: ")
            quantity = int(input("Enter quantity: "))
            result = parlor.add_to_cart(flavor_name, quantity)
            if result:
                print("Added to cart successfully!")
            else:
                print("Failed to add to cart.")
        
        elif choice == '3':
            cart_items = parlor.view_cart()
            for name, qty, total in cart_items:
                print(f"{name}: {qty} x Total: ${total:.2f}")
        
        elif choice == '4':
            parlor.clear_cart()
            print("Cart cleared!")
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
