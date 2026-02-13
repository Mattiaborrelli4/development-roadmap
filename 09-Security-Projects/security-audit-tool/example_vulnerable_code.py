"""
EXAMPLE VULNERABLE CODE FOR EDUCATIONAL PURPOSES
Questo codice contiene VULNERABILITÀ INTENZIONALI
Da usare SOLO per testare lo Security Audit Tool
"""

# ============================================
# VULNERABILITÀ 1: SQL Injection
# ============================================

import sqlite3

def vulnerable_query(user_id):
    """❌ VULNERABLE - SQL Injection"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Vulnerable: f-string with user input
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    return cursor.fetchall()

def safe_query(user_id):
    """✅ SAFE - Parameterized query"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Safe: parameterized query
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cursor.fetchall()


# ============================================
# VULNERABILITÀ 2: XSS (Cross-Site Scripting)
# ============================================

from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    """❌ VULNERABLE - XSS"""
    user_name = request.args.get('name', '')

    # Vulnerable: direct output of user input
    return f"<h1>Hello {user_name}!</h1>"

@app.route('/safe_hello')
def safe_hello():
    """✅ SAFE - Escaped output"""
    import html
    user_name = request.args.get('name', '')

    # Safe: escaped output
    return f"<h1>Hello {html.escape(user_name)}!</h1>"


# ============================================
# VULNERABILITÀ 3: Hardcoded Credentials
# ============================================

class Config:
    """❌ VULNERABLE - Hardcoded credentials"""

    # Vulnerable: hardcoded password
    DB_PASSWORD = "mysupersecretpassword123"
    API_KEY = "sk_test_FAKE_EXAMPLE_KEY_DO_NOT_USE_12345"

    # Vulnerable: AWS keys (EXAMPLE from AWS docs)
    AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


class SafeConfig:
    """✅ SAFE - Environment variables"""
    import os

    # Safe: from environment
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    API_KEY = os.environ.get('API_KEY')


# ============================================
# VULNERABILITÀ 4: Weak Cryptography
# ============================================

import hashlib

def weak_hash(data):
    """❌ VULNERABLE - Weak hash"""
    # Vulnerable: MD5 is broken
    return hashlib.md5(data.encode()).hexdigest()

def strong_hash(data):
    """✅ SAFE - Strong hash"""
    # Safe: SHA-256 is strong
    return hashlib.sha256(data.encode()).hexdigest()


# ============================================
# VULNERABILITÀ 5: Insecure Random
# ============================================

import random

def weak_token():
    """❌ VULNERABLE - Insecure random"""
    # Vulnerable: random is not cryptographically secure
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=32))

def strong_token():
    """✅ SAFE - Secure random"""
    import secrets
    # Safe: secrets is cryptographically secure
    return secrets.token_urlsafe(32)


# ============================================
# VULNERABILITÀ 6: Missing Input Validation
# ============================================

def vulnerable_login():
    """❌ VULNERABLE - No validation"""
    user_id = request.GET.get('id')
    username = request.POST.get('username')

    # No validation of input
    # Could be empty, wrong type, too long, etc.
    return f"User {username} with ID {user_id}"

def safe_login():
    """✅ SAFE - With validation"""
    try:
        user_id = int(request.GET.get('id', 0))
        username = request.POST.get('username', '').strip()

        if not (0 < len(username) <= 50):
            raise ValueError("Invalid username length")

        return f"User {username} with ID {user_id}"
    except (ValueError, TypeError):
        return "Invalid input"


# ============================================
# VULNERABILITÀ 7: Command Injection
# ============================================

import os

def vulnerable_ping(host):
    """❌ VULNERABLE - Command injection"""
    # Vulnerable: user input in command
    os.system(f"ping -c 4 {host}")

def safe_ping(host):
    """✅ SAFE - Sanitized input"""
    import subprocess

    # Validate host is just a hostname/IP
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        raise ValueError("Invalid host")

    # Safe: no shell=True
    subprocess.run(['ping', '-c', '4', host], check=True)


# ============================================
# VULNERABILITÀ 8: Path Traversal
# ============================================

def vulnerable_read_file(filename):
    """❌ VULNERABLE - Path traversal"""
    # Vulnerable: no path validation
    with open(f'/var/www/{filename}', 'r') as f:
        return f.read()

def safe_read_file(filename):
    """✅ SAFE - Path validation"""
    import os

    # Safe: validate and sanitize path
    base_dir = '/var/www/'
    filepath = os.path.normpath(os.path.join(base_dir, filename))

    if not filepath.startswith(base_dir):
        raise ValueError("Invalid path")

    with open(filepath, 'r') as f:
        return f.read()


# ============================================
# VULNERABILITÀ 9: SSRF (Server-Side Request Forgery)
# ============================================

import requests

def vulnerable_fetch(url):
    """❌ VULNERABLE - SSRF"""
    # Vulnerable: user-controlled URL
    return requests.get(url).text

def safe_fetch(url):
    """✅ SAFE - URL validation"""
    from urllib.parse import urlparse

    # Validate URL
    parsed = urlparse(url)

    # Only allow specific domains
    allowed_domains = ['api.example.com', 'cdn.example.com']
    if parsed.netloc not in allowed_domains:
        raise ValueError("URL not allowed")

    return requests.get(url).text


# ============================================
# VULNERABILITÀ 10: Deserialization
# ============================================

import pickle

def vulnerable_deserialize(data):
    """❌ VULNERABLE - Unsafe deserialization"""
    # Vulnerable: pickle can execute arbitrary code
    return pickle.loads(data)

def safe_deserialize(data):
    """✅ SAFE - JSON deserialization"""
    import json
    # Safe: JSON is data-only
    return json.loads(data)


if __name__ == '__main__':
    print("⚠️  Questo file contiene codice VULNERABILE!")
    print("Usalo SOLO per testare lo Security Audit Tool")
    print("NON usarlo mai in produzione!")
