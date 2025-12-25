#!C:/Users/python/AppData/Local/Programs/Python/Python311/python
import cgi
import cgitb
import json
from pymongo import MongoClient

cgitb.enable()

print("Content-Type: application/json")
print()

# Read JSON from POST
import sys
try:
    data_json = sys.stdin.read()
    data = json.loads(data_json)
except:
    print(json.dumps({"status": "error", "message": "Invalid JSON"}))
    exit()

# Connect MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["grocery_db"]
collection = db["products"]

# Validation
required_fields = ["id","name","desc","old","price","colors","images"]
for f in required_fields:
    if f not in data or not data[f]:
        print(json.dumps({"status":"error","message":f"Field {f} is required"}))
        exit()

# Validate images count
if len(data["images"]) < 3:
    print(json.dumps({"status":"error","message":"At least 3 images are required"}))
    exit()

# Insert product
try:
    collection.insert_one({
        "id": int(data.get("id")),
        "name": data.get("name"),
        "desc": data.get("desc"),
        "old": data.get("old"),
        "price": data.get("price"),
        "colors": data.get("colors"),
        "images": data.get("images")
    })
    print(json.dumps({"status":"success","message":"Product added successfully!"}))
except Exception as e:
    print(json.dumps({"status":"error","message":str(e)}))
