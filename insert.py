from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")  # default local connection
db = client['grocery_db']  # Database
collection = db['products']  # Collection

# Your products data
products = [
    {"id":1,"name":"Basmati Rice 5kg","old":"₹480","price":"₹420","desc":"Premium quality long grain rice","colors": ["White"],
     "images":["https://www.bbassets.com/media/uploads/p/l/255843_20-daawat-super-basmati-5-kg.jpg",
               "https://www.bbassets.com/media/uploads/p/l/255843-2_5-daawat-super-basmati-5-kg.jpg","https://www.bbassets.com/media/uploads/p/l/255843-4_5-daawat-super-basmati-5-kg.jpg"]},
    {"id":2,"name":"Wheat Flour 10kg","old":"₹560","price":"₹510","desc":"Fresh chakki atta","colors": ["Light Brown"],
     "images":["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRnM9UTuG0j5E-77aobzGSb15BZdDaJiiMmw&s","https://via.placeholder.com/300?text=Flour2"]},
    {"id":3,"name":"Sunflower Oil 1L","old":"₹190","price":"₹165","desc":"Healthy cooking oil","colors": ["Golden Yellow"],
     "images":["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeTKXLuM-mSKHYojUlUmch9LLmBXXsb8Ix9w&s"]},
    {"id":4,"name":"Toor Dal 1kg","old":"₹170","price":"₹145","desc":"High protein dal","colors": ["Yellow"],
     "images":["https://www.jamoona.com/cdn/shop/files/TRS-1kg-Toor-Dal--Toor-Linsen--991608.png?v=1753206972"]},
    {"id":5,"name":"Sugar 2kg","old":"₹115","price":"₹98","desc":"Pure crystal sugar","colors": ["White"],
     "images":["https://5.imimg.com/data5/SELLER/Default/2025/1/484754662/XE/QP/JX/221376662/amrut-white-crystal-sugar-2kg.jpeg"]},
    {"id":6,"name":"Salt 1kg","old":"₹30","price":"₹22","desc":"Iodized salt","colors": ["White"],
     "images":["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfoaWTj2sfTOp1UB8shPe5y_gRT8WRPSoDww&s"]},
    {"id":7,"name":"Tea Powder 500g","old":"₹290","price":"₹260","desc":"Strong tea leaves","colors": ["Black", "Dark Brown"],
     "images":["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU1DtPhyBRZ0utf_CNy0gBKXVdeAjEdtyQGw&s"]},
    {"id":8,"name":"Coffee 200g","old":"₹220","price":"₹195","desc":"Premium coffee","colors": ["Dark Brown", "Black"],
     "images":["https://shop.tulsidas.com/cdn/shop/products/nescafe-matinal-coffee-200g-smooth-balanced-coffee-344251_grande.jpg?v=1685168729"]},
    {"id":9,"name":"Cooking Oil 5L","old":"₹820","price":"₹750","desc":"Family pack oil","colors": ["Golden Yellow"],
     "images":["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ21qQOOkoiA9gk3E2sHMWmFlipRmMc2AdS-w&s"]},
    {"id":10,"name":"Milk Powder 1kg","old":"₹410","price":"₹375","desc":"Rich milk powder","colors": ["Off White", "Cream"],
     "images":["https://m.media-amazon.com/images/I/71fwfzc-iSL._AC_UF894,1000_QL80_.jpg"]},
    {"id":11,"name":"Chana Dal 1kg","old":"₹200","price":"₹175","desc":"High quality chana dal","colors":["Yellow"],
     "images":["https://www.jiomart.com/images/product/original/491187252/good-life-chana-dal-1-kg-product-images-o491187252-p491187252-2-202208181542.jpg?im=Resize=(420,420)"]},
    {"id":12,"name":"Moong Dal 1kg","old":"₹220","price":"₹190","desc":"Healthy moong dal","colors":["Yellow"],
     "images":["https://www.jiomart.com/images/product/original/492851046/good-life-unpolished-moong-dal-1-kg-product-images-o492851046-p591219170-0-202301252150.jpg?im=Resize=(1000,1000)"]},
    {"id":13,"name":"Masoor Dal 1kg","old":"₹210","price":"₹185","desc":"Premium masoor dal","colors":["Red"],
     "images":["https://www.jiomart.com/images/product/original/492851049/good-life-unpolished-masoor-dal-1-kg-product-images-o492851049-p591219173-0-202301252136.jpg"]},
    {"id":14,"name":"Besan 1kg","old":"₹150","price":"₹130","desc":"Fine gram flour","colors":["Yellow"],
     "images":["https://bajarhaat.com/wp-content/uploads/2024/06/Fortune-chana-besan.jpg"]},
    {"id":15,"name":"Refined Oil 1L","old":"₹180","price":"₹160","desc":"Pure cooking oil","colors":["Golden Yellow"],
     "images":["https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_600/e7b2e9e35ff9cdcb52d04277795c0304"]},
    {"id":16,"name":"Ghee 1L","old":"₹600","price":"₹550","desc":"Pure cow ghee","colors":["Yellow"],
     "images":["https://www.quickpantry.in/cdn/shop/products/amul-pure-ghee-1-l-tin-quick-pantry.jpg?v=1710539178"]},
    {"id":17,"name":"Paneer 500g","old":"₹250","price":"₹220","desc":"Fresh paneer","colors":["White"],
     "images":["https://5.imimg.com/data5/ECOM/Default/2023/3/293749064/QN/UA/BA/61114009/3d-paneer-500g-tilt-left-1.png"]},
    {"id":18,"name":"Curd 1kg","old":"₹90","price":"₹75","desc":"Fresh curd","colors":["White"],
     "images":["https://m.media-amazon.com/images/I/61aeyWGZhpL.jpg"]},
    {"id":19,"name":"Eggs 12pcs","old":"₹120","price":"₹100","desc":"Farm fresh eggs","colors":["Brown"],
     "images":["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIDoyMzkUni0s-MUPR-LXsgOnivQY9Pp3dPw&s"]},
    {"id":20,"name":"Chicken 1kg","old":"₹300","price":"₹270","desc":"Fresh chicken","colors":["White","Pink"],
     "images":["https://udupifresh.com/cdn/shop/products/Chicken-CurryCutWithoutSkin_1_8816e378-a039-4a14-bb03-7b14618872bd_1200x1200.jpg?v=1673205494"]},
]

# Insert products into MongoDB
collection.insert_many(products)

print("Products inserted successfully!")