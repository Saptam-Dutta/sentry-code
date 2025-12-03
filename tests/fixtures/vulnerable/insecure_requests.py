import requests
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
