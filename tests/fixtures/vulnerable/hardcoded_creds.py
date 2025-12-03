"""VULNERABLE: Hardcoded credentials"""

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
