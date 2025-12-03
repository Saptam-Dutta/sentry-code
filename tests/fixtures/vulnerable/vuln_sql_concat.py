import sqlite3

def get_user_data(username):
    """VULNERABLE: SQL Injection via string concatenation"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # VULN: PY002 - String concatenation in SQL query
    query = "SELECT * FROM users WHERE username = " + "'" + username + "'"
    cursor.execute(query)
    
    return cursor.fetchall()

def search_products(category):
    """VULNERABLE: SQL Injection via f-string"""
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    
    # VULN: PY002 - f-string formatting
    query = f"SELECT * FROM products WHERE category = '{category}'"
    cursor.execute(query)
    
    return cursor.fetchall()
