import pandas as pd
import os
import hashlib
import json

# Path to users database file
USERS_DB_PATH = "data/users.json"

def _hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def _init_users_db():
    """Initialize users database if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(USERS_DB_PATH):
        with open(USERS_DB_PATH, "w") as f:
            json.dump({}, f)

def validate_login(username, password, role):
    """Validate user login credentials"""
    _init_users_db()
    
    if not username or not password:
        return False
    
    with open(USERS_DB_PATH, "r") as f:
        users = json.load(f)
    
    hashed_password = _hash_password(password)
    
    if username in users and users[username]["password"] == hashed_password and users[username]["role"] == role:
        return True
    return False

def register_user(username, password, role):
    """Register a new user"""
    _init_users_db()
    
    if not username or not password:
        return "❌ Username and password are required."
    
    with open(USERS_DB_PATH, "r") as f:
        users = json.load(f)
    
    if username in users:
        return "❌ Username already exists. Please choose another one."
    
    users[username] = {
        "password": _hash_password(password),
        "role": role
    }
    
    with open(USERS_DB_PATH, "w") as f:
        json.dump(users, f)
    
    return "🎉 Successfully signed up! Please log in to continue."
