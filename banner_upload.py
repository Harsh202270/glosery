import firebase_admin
from firebase_admin import credentials, db

# 🔑 Load Firebase service account key
cred = credentials.Certificate("firebase_key.json")

# 🔥 Initialize Firebase (DO THIS ONCE)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://product-41d50-default-rtdb.firebaseio.com/"
})

# 📌 Banner image URLs to store
banner_images = [
    "https://www.shutterstock.com/shutterstock/photos/2362872835/display_1500/stock-vector-supermarket-template-groceries-grocery-store-shopping-supermarket-fresh-food-home-delivery-2362872835.jpg",
    "https://kalidas365itsolutions.wordpress.com/wp-content/uploads/2014/06/banner6.jpg?w=768",
    "https://www.shutterstock.com/shutterstock/photos/2443027609/display_1500/stock-vector-always-fresh-fruits-and-veggies-banner-template-vector-apple-icon-background-salad-leaf-2443027609.jpg"
]

# 📂 Reference to banners branch
ref = db.reference("banners")

# 🚀 Upload banners
for img in banner_images:
    ref.push(img)

print("✅ All banners uploaded successfully!")
