from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import uuid
from datetime import datetime

# ================= APP SETUP =================
app = Flask(__name__)
CORS(app)

# ================= FIREBASE INIT =================
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://product-41d50-default-rtdb.firebaseio.com/"
})

# ================= ADD PRODUCT API =================
@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.json

    # Required fields including stock and expiry
    required = ["id", "name", "desc", "old", "price", "colors", "images", "stock", "expiryDate"]
    for r in required:
        if r not in data or not data[r]:
            return jsonify({
                "status": "error",
                "message": f"Field '{r}' is mandatory"
            }), 400

    # Validate stock
    try:
        stock = int(data["stock"])
        if stock < 1:
            return jsonify({"status":"error","message":"Stock must be at least 1"}), 400
    except:
        return jsonify({"status":"error","message":"Stock must be a valid number"}), 400

    # Validate expiry date format YYYY-MM-DD
    try:
        expiry = datetime.strptime(data["expiryDate"], "%Y-%m-%d").isoformat()
    except:
        return jsonify({"status":"error","message":"Expiry date must be in YYYY-MM-DD format"}), 400

    # Prepare product data
    product = {
        "id": data["id"],
        "name": data["name"],
        "desc": data["desc"],
        "old": data["old"],
        "price": data["price"],
        "colors": data["colors"],
        "images": data["images"],
        "stock": stock,
        "expiryDate": expiry,
        "createdAt": datetime.now().isoformat()
    }

    # Push to Firebase
    ref = db.reference("Products")
    ref.push(product)

    return jsonify({
        "status": "success",
        "message": "Product added successfully",
        "product": product
    })

# ================= PRODUCTS API =================
@app.route("/products", methods=["GET"])
def get_products():
    ref = db.reference("Products")
    products = ref.get() or []
    if isinstance(products, dict):
        products = list(products.values())
    return jsonify(products)

# ================= BANNERS API =================
@app.route("/banners", methods=["GET"])
def get_banners():
    ref = db.reference("banners")
    banners = ref.get()
    if banners is None:
        return jsonify([])
    if isinstance(banners, dict):
        banners = list(banners.values())
    return jsonify(banners)

# ================= USER API =================
@app.route("/user", methods=["POST"])
def user_handler():
    data = request.json
    action = data.get("action")
    users_ref = db.reference("Users")
    users = users_ref.get() or {}

    # ---------- SIGN UP ----------
    if action == "signup":
        name = data.get("name")
        email = data.get("email", "").strip().lower()
        phone = data.get("phone")
        password = data.get("password")

        if not name or not email or not phone or not password:
            return jsonify({"status": "error", "message": "All fields are required"})

        for u in users.values():
            if u.get("email") == email:
                return jsonify({"status": "error", "message": "Email already registered"})

        user_id = str(uuid.uuid4())
        users_ref.child(user_id).set({
            "id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "password": password
        })

        return jsonify({
            "status": "success",
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "phone": phone
            }
        })

    # ---------- SIGN IN ----------
    elif action == "signin":
        email = data.get("email", "").strip().lower()
        password = str(data.get("password")).strip()

        for u in users.values():
            if u.get("email") == email and str(u.get("password")) == password:
                return jsonify({
                    "status": "success",
                    "user": {
                        "id": u["id"],
                        "name": u["name"],
                        "email": u["email"],
                        "phone": u["phone"]
                    }
                })

        return jsonify({"status": "error", "message": "Invalid email or password"})

    # ---------- FORGOT PASSWORD ----------
    elif action == "forgot_password":
        email = data.get("email", "").strip().lower()
        phone = data.get("phone")
        new_password = data.get("new_password")

        for user_id, u in users.items():
            if u.get("email") == email:

                if phone and u.get("phone") != phone:
                    return jsonify({"status": "error", "message": "Phone number does not match"})

                if new_password:
                    users_ref.child(user_id).update({"password": new_password})
                    return jsonify({"status": "success", "message": "Password updated successfully"})

                return jsonify({"status": "success", "message": "Email verified"})

        return jsonify({"status": "error", "message": "Email is not registered"})

    return jsonify({"status": "error", "message": "Invalid action"})

# ================= UPDATE STOCK API =================
@app.route("/update-stock", methods=["POST"])
def update_stock():
    data = request.json
    items = data.get("items", [])

    if not items:
        return jsonify({"status": "error", "message": "No items provided"}), 400

    products_ref = db.reference("Products")
    products = products_ref.get() or []

    updated_items = []

    for item in items:
        product_id = item.get("id")
        qty = int(item.get("qty", 1))

        for key, product in (products.items() if isinstance(products, dict) else enumerate(products)):
            if product and product.get("id") == product_id:
                current_stock = int(product.get("stock", 0))
                new_stock = max(current_stock - qty, 0)

                # Update in Firebase
                products_ref.child(str(key)).update({"stock": new_stock})

                updated_items.append({
                    "id": product_id,
                    "old_stock": current_stock,
                    "new_stock": new_stock
                })
                break

    return jsonify({
        "status": "success",
        "updated": updated_items
    })

# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True)
