"""
database.py
------------
This script sets up our database. A database is just an organized way to
store data permanently (unlike variables in code, which disappear when the
program stops).

We're using SQLite here because it's the simplest database to start with:
it's just a single file on disk, no separate server needed to run it.
Later, for a real production app, you'd likely move to PostgreSQL — but
SQLite is perfect for learning and even for small real apps.
"""

import sqlite3

def get_connection():
    """Opens a connection to our database file (creates it if it doesn't exist)."""
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["name"]
    return conn

def init_db():
    """Creates the products table and fills it with starter data.
    Run this once (or whenever you want to reset the data)."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create the table structure — this defines what a "product" looks like in our database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            price REAL NOT NULL,
            emoji TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Check if we already have products — don't duplicate them every time this runs
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        starter_products = [
            ("Bananas", "1 dozen", 45, "🍌", "Fruits"),
            ("Apples", "1 kg", 180, "🍎", "Fruits"),
            ("Mangoes", "1 kg", 120, "🥭", "Fruits"),
            ("Tomatoes", "1 kg", 40, "🍅", "Vegetables"),
            ("Onions", "1 kg", 35, "🧅", "Vegetables"),
            ("Potatoes", "1 kg", 30, "🥔", "Vegetables"),
            ("Spinach", "250 g", 25, "🥬", "Vegetables"),
            ("Milk", "1 L", 60, "🥛", "Dairy"),
            ("Eggs", "12 pcs", 84, "🥚", "Dairy"),
            ("Paneer", "200 g", 90, "🧀", "Dairy"),
            ("Basmati Rice", "5 kg", 450, "🍚", "Staples"),
            ("Wheat Atta", "5 kg", 260, "🌾", "Staples"),
            ("Cooking Oil", "1 L", 150, "🛢️", "Staples"),
            ("Wireless Earbuds", "1 pc", 1499, "🎧", "Electronics"),
            ("Phone Charger", "1 pc", 399, "🔌", "Electronics"),
            ("LED Bulb", "1 pc", 99, "💡", "Electronics"),
            ("Notebook Set", "5 pcs", 150, "📓", "Stationery"),
            ("Ballpoint Pens", "10 pcs", 60, "🖊️", "Stationery"),
            ("Dish Soap", "500 ml", 85, "🧴", "Household"),
            ("Toilet Paper", "6 rolls", 180, "🧻", "Household"),
        ]
        cursor.executemany(
            "INSERT INTO products (name, unit, price, emoji, category) VALUES (?, ?, ?, ?, ?)",
            starter_products
        )
        print(f"Added {len(starter_products)} starter products to the database.")
    else:
        print(f"Database already has {count} products. Skipping seed data.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database ready: store.db")
