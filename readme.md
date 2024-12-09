# Ice Cream Parlor Management Application

## Overview
This is a Python-based management application for an ice cream parlor cafe. The application uses SQLAlchemy with SQLite to manage seasonal flavor offerings, ingredient inventory, and customer preferences.

## Features
- Add and manage flavors
- Track ingredient inventory
- Manage allergen information
- Add items to cart
- Search and filter flavors
- View and clear cart

## Prerequisites
- Python 3.9+
- Docker (optional)

## Installation

### Local Setup
1. Clone the repository
2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application
   ```bash
   python main.py
   ```

### Docker Setup
1. Build the Docker image
   ```bash
   docker build -t ice-cream-parlor .
   ```
2. Run the Docker container
   ```bash
   docker run -it ice-cream-parlor
   ```

## Testing Steps
1. Add a new allergen (e.g., "Peanuts")
2. Add a new flavor with ingredients and allergens
3. Search for flavors:
   - All flavors
   - Seasonal flavors
   - By name
4. Add items to cart
5. View cart contents
6. Clear cart

## Database Schema
- **Flavors**: Store ice cream flavor details
- **Ingredients**: Track ingredient inventory
- **Allergens**: Manage allergen information
- **Cart**: Temporary storage for selected items
