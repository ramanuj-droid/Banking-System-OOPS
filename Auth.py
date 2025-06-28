import json
import hashlib
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

#Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register
def signup(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    
    users[username] = hash_password(password)
    save_users(users)
    return True, "User registered successfully."

#login
def login(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True, "Login successful."
    else:
        return False, "Invalid username or password."
