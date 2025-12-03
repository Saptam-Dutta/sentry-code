import sqlite3

def get_user_data_safe(username):
    """SAFE: Using parameterized query"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Safe: Parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    return cursor.fetchall()

def search_products_safe(category):
    """SAFE: Using named parameters"""
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    
    query = "SELECT * FROM products WHERE category = :category"
    cursor.execute(query, {"category": category})
    
    return cursor.fetchall()
