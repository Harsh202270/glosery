import firebase_admin
from firebase_admin import credentials, db
import random
from datetime import datetime, timedelta

# 🔑 Firebase service account key
cred = credentials.Certificate("firebase_key.json")

# 🔥 Initialize Firebase
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://product-41d50-default-rtdb.firebaseio.com/"
})

# 📦 Reference to Products
products_ref = db.reference("Products")
products = products_ref.get()

if not products:
    print("❌ No products found")
    exit()

updated = 0
today = datetime.now()

for index, product in enumerate(products):
    # Skip null entries
    if product is None:
        continue

    # 📅 Random expiry date (6–24 months from today)
    months = random.randint(6, 24)
    expiry_date = today + timedelta(days=months * 30)
    expiry_str = expiry_date.strftime("%Y-%m-%d")

    # 🔄 Update ONLY expiry
    products_ref.child(str(index)).update({
        "expiry": expiry_str
    })

    updated += 1
    print(f"✅ Product ID {product.get('id')} → Expiry: {expiry_str}")

print(f"\n🎉 Expiry date added to {updated} products successfully")
