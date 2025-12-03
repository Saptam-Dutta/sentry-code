import os

# Ensure directory exists
os.makedirs("tests/fixtures/vulnerable", exist_ok=True)
os.makedirs("tests/fixtures/clean", exist_ok=True)

# vuln_sql_concat.py
sql_content = '''import sqlite3

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
'''

with open("tests/fixtures/vulnerable/vuln_sql_concat.py", "w", encoding="utf-8") as f:
    f.write(sql_content)

# hardcoded_creds.py
creds_content = '''"""VULNERABLE: Hardcoded credentials"""

# VULN: PY001 - Hardcoded API key
API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

class DatabaseConnection:
    def __init__(self):
        # VULN: PY001 - Hardcoded password
        self.password = "SuperSecret123!"
        self.username = "admin"
    
    def connect(self):
        # VULN: PY001 - Hardcoded token
        auth_token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
        return f"Connected with {auth_token}"

def authenticate(user_password):
    # VULN: PY001 - Password in code
    admin_password = "P@ssw0rd2024!"
    return user_password == admin_password
'''

with open("tests/fixtures/vulnerable/hardcoded_creds.py", "w", encoding="utf-8") as f:
    f.write(creds_content)

# vuln_exec.py
exec_content = '''"""VULNERABLE: Use of eval and exec on user input"""

def calculate_expression(user_input):
    """VULN: PY003 - eval() on untrusted input"""
    result = eval(user_input)
    return result

def execute_code(code_string):
    """VULN: PY003 - exec() on untrusted input"""
    exec(code_string)

def dynamic_import(module_name):
    """VULN: PY003 - eval for imports"""
    mod = eval(f"__import__({module_name})")
    return mod

class Calculator:
    def compute(self, formula):
        # VULN: PY003 - eval in class method
        return eval(formula)
'''

with open("tests/fixtures/vulnerable/vuln_exec.py", "w", encoding="utf-8") as f:
    f.write(exec_content)

# insecure_requests.py
requests_content = '''import requests
import hashlib

def fetch_data(url):
    """VULN: PY004 - SSL verification disabled"""
    response = requests.get(url, verify=False)
    return response.json()

def download_file(url):
    """VULN: PY004 - Disabled certificate check"""
    r = requests.get(url, verify=False, timeout=10)
    return r.content

def hash_password(password):
    """VULN: PY007 - Weak hash function"""
    return hashlib.md5(password.encode()).hexdigest()

def legacy_hash(data):
    """VULN: PY007 - SHA1 usage"""
    return hashlib.sha1(data.encode()).hexdigest()
'''

with open("tests/fixtures/vulnerable/insecure_requests.py", "w", encoding="utf-8") as f:
    f.write(requests_content)

# command_injection.py
command_content = '''import os
import subprocess

def run_command(user_input):
    """VULN: PY005 - Command injection via os.system"""
    os.system("ls " + user_input)

def execute_shell(filename):
    """VULN: PY005 - Shell command with user input"""
    os.system(f"cat {filename}")

def backup_file(path):
    """VULN: PY005 - subprocess with shell=True"""
    subprocess.call("cp " + path + " /backup/", shell=True)
'''

with open("tests/fixtures/vulnerable/command_injection.py", "w", encoding="utf-8") as f:
    f.write(command_content)

# safe_sql.py (clean file)
safe_sql_content = '''import sqlite3

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
'''

with open("tests/fixtures/clean/safe_sql.py", "w", encoding="utf-8") as f:
    f.write(safe_sql_content)

print("✓ All test files created successfully without BOM!")

# Verify files
import os
files = [
    "tests/fixtures/vulnerable/vuln_sql_concat.py",
    "tests/fixtures/vulnerable/hardcoded_creds.py",
    "tests/fixtures/vulnerable/vuln_exec.py",
    "tests/fixtures/vulnerable/insecure_requests.py",
    "tests/fixtures/vulnerable/command_injection.py",
    "tests/fixtures/clean/safe_sql.py"
]

print("\nVerifying files:")
for filepath in files:
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✓ {filepath}: {size} bytes")
    else:
        print(f"  ✗ {filepath}: NOT FOUND")
