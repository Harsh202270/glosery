#!C:/Users/python/AppData/Local/Programs/Python/Python311/python
import sys
import json
from pymongo import MongoClient
import cgitb
cgitb.enable()

# ------------------- HEADER -------------------
print("Content-Type: application/json\n")  # Only once

# ------------------- READ JSON INPUT -------------------
try:
    raw_input = sys.stdin.read()
    data = json.loads(raw_input)
except:
    print(json.dumps({"status":"error","message":"Invalid JSON"}))
    sys.exit()

# ------------------- MONGO CONNECTION -------------------
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["grocery_db"]
    users = db["users"]
except:
    print(json.dumps({"status":"error","message":"MongoDB connection failed"}))
    sys.exit()

action = data.get("action", "").strip().lower()

# ------------------- SIGN UP -------------------
if action == "signup":
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    password = data.get("password", "").strip()

    if not all([name, email, phone, password]):
        print(json.dumps({"status":"error","message":"All fields are required"}))
        sys.exit()

    if users.find_one({"email": email}):
        print(json.dumps({"status":"error","message":"Email already exists"}))
        sys.exit()

    users.insert_one({
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    })

    print(json.dumps({"status":"success","message":"Signup successful"}))

# ------------------- SIGN IN -------------------
elif action == "signin":
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        print(json.dumps({"status":"error","message":"Email and password required"}))
        sys.exit()

    user = users.find_one({"email": email, "password": password}, {"_id":0})

    if not user:
        print(json.dumps({"status":"error","message":"Invalid email or password"}))
        sys.exit()

    print(json.dumps({
        "status":"success",
        "message":"Login successful",
        "user":{
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone")
        }
    }))

# ------------------- GET PROFILE -------------------
elif action == "profile":
    email = data.get("email", "").strip()
    if not email:
        print(json.dumps({"status":"error","message":"Email required"}))
        sys.exit()

    user = users.find_one({"email": email}, {"_id":0, "password":0})
    if not user:
        print(json.dumps({"status":"error","message":"User not found"}))
        sys.exit()

    print(json.dumps({"status":"success","profile":user}))

# ------------------- LOGOUT -------------------
elif action == "logout":
    # For now just return success; session handling can be added later
    print(json.dumps({"status":"success","message":"Logged out successfully"}))

# ------------------- INVALID ACTION -------------------
else:
    print(json.dumps({"status":"error","message":"Invalid action"}))
