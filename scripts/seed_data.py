import sys
import os
import random
from datetime import date, timedelta
from random import randint

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.transactions.models import Transaction, TransactionCategory
from config import config

# Setup Flask App Context
ENV = os.getenv('FLASK_ENV', 'development')
app_config = config[ENV]
app = create_app(app_config)

def seed_data():
    with app.app_context():
        print("Starting data seeding...")

        # 1. Ensure Categories exist
        categories_data = [
            "Food & Drink",
            "Transportation",
            "Shopping",
            "Entertainment",
            "Housing",
            "Medical",
            "Investment"
        ]
        
        categories_map = {}
        for cat_name in categories_data:
            cat = TransactionCategory.query.filter_by(name=cat_name).first()
            if not cat:
                cat = TransactionCategory(name=cat_name)
                db.session.add(cat)
                print(f"Created category: {cat_name}")
            categories_map[cat_name] = cat
        
        db.session.commit()
        
        # Reload categories to get IDs
        categories = TransactionCategory.query.all()
        
        # 2. Generate Transactions for the last 30 days
        start_date = date.today() - timedelta(days=30)
        items_pool = {
            "Food & Drink": ["Lunch", "Dinner", "Coffee", "Brunch", "Snacks", "Bubble Tea", "Steak house"],
            "Transportation": ["MRT", "Bus", "Taxi/Uber", "Gas", "Parking"],
            "Shopping": ["Groceries", "Clothes", "Electronics", "Amazon", "Books"],
            "Entertainment": ["Movie", "Netflix Subscription", "Spotify", "Mobile Game", "Concert"],
            "Housing": ["Rent", "Electricity Bill", "Water Bill", "Internet"],
            "Medical": ["Pharmacy", "Clinic", "Gym"],
            "Investment": ["Stock Purchase", "ETF"]
        }

        generated_count = 0
        current_date = start_date
        today = date.today()

        while current_date <= today:
            # Randomly decide how many transactions for this day (0 to 5)
            daily_tx_count = randint(1, 5)
            
            for _ in range(daily_tx_count):
                # Pick a random category
                cat = random.choice(categories)
                
                # Pick a random item based on category
                possible_items = items_pool.get(cat.name, ["Misc"])
                item_name = random.choice(possible_items)
                
                # Random expense amount (weighted differently for logical valid)
                if cat.name == "Housing":
                     # Rent or bills usually happen once, but for simulation let's make them higher
                     amount = randint(1000, 5000)
                elif cat.name == "Food & Drink":
                     amount = randint(50, 500)
                else:
                     amount = randint(100, 2000)

                new_tx = Transaction(
                    item=item_name,
                    category_id=cat.id,
                    expense=amount,
                    transaction_at=current_date,
                    remark=f"Auto-generated record for {current_date}"
                )
                db.session.add(new_tx)
                generated_count += 1
            
            current_date += timedelta(days=1)

        db.session.commit()
        print(f"Successfully added {generated_count} transactions across the last 30 days.")

if __name__ == "__main__":
    seed_data()
