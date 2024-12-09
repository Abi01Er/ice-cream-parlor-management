from crud import IceCreamParlor
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
