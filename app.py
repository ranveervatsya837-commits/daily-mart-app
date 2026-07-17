"""
app.py
------
This is your backend server. It does three jobs:
  1. Serves your webpage (index.html) to the browser
  2. Provides an "API" — URLs that return data (products) as JSON, which
     your JavaScript on the frontend can fetch and display
  3. Talks to the database to read/write product data

Run this file, then open http://localhost:5000 in your browser.
"""

from flask import Flask, jsonify, render_template, request
from database import get_connection, init_db

app = Flask(__name__)

# ---------- PAGE ROUTE ----------
# This serves the actual HTML page when someone visits the site.
@app.route("/")
def home():
    return render_template("index.html")


# ---------- API ROUTES ----------
# These don't return web pages — they return raw data (JSON) that
# JavaScript in the browser can use. This is how frontend and backend
# talk to each other in almost every real web app.

@app.route("/api/products")
def get_products():
    """Returns all products, or filters by category/search if provided.
    Example: /api/products?category=Fruits&search=apple
    """
    category = request.args.get("category", "All")
    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE name LIKE ?"
    params = [f"%{search}%"]

    if category != "All":
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # Convert database rows into plain dictionaries so they can become JSON
    products = [dict(row) for row in rows]
    return jsonify(products)


@app.route("/api/categories")
def get_categories():
    """Returns the list of unique categories, for building the filter bar."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = [row["category"] for row in cursor.fetchall()]
    conn.close()
    return jsonify(["All"] + categories)


if __name__ == "__main__":
    init_db()  # make sure the database exists and has data before starting
    app.run(debug=True, port=5000)
