import pymysql

# Connect to database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='111222333',
    database='grocery_db'
)
cursor = conn.cursor()

# Product-specific images mapping based on actual product names
product_images = {
    # Fruits
    'Organic Bananas': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400',
    'Green Apples': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400',
    'Red Apples': 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=400',
    'Strawberries': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400',
    'Oranges': 'https://images.unsplash.com/photo-1547514701-42782101795e?w=400',
    'Blueberries': 'https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=400',
    'Grapes': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400',
    
    # Dairy
    'Whole Milk': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400',
    'Cheddar Cheese': 'https://images.unsplash.com/photo-1452195100486-9cc805987862?w=400',
    'Greek Yogurt': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400',
    'Butter': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400',
    
    # Bakery
    'Whole Wheat Bread': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400',
    'Bagels': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400',
    'Croissants': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400',
    
    # Meat
    'Chicken Breast': 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400',
    'Ground Beef': 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400',
    'Pork Chops': 'https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=400',
    
    # Seafood
    'Salmon Fillet': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400',
    'Shrimp': 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=400',
    
    # Vegetables  
    'Carrots': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400',
    'Broccoli': 'https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=400',
    'Tomatoes': 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=400',
    'Lettuce': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=400',
    'Potatoes': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400',
    'Onions': 'https://images.unsplash.com/photo-1508747703725-719777637510?w=400',
    
    # Snacks
    'Potato Chips': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400',
    'Chocolate Bar': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400',
    'Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400',
    
    # Beverages
    'Orange Juice': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400',
    'Coffee': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400',
    'Tea': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400',
    'Soda': 'https://images.unsplash.com/photo-1581006852262-e4307cf6283a?w=400',
}

# Category fallback images
category_images = {
    'Fruits': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400',
    'Dairy': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400',
    'Bakery': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400',
    'Meat': 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400',
    'Seafood': 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=400',
    'Vegetables': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400',
    'Snacks': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=400',
    'Beverages': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400',
    'Pantry': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400',
    'Frozen': 'https://images.unsplash.com/photo-1628028811775-7c8e67db5eec?w=400',
    'Household': 'https://images.unsplash.com/photo-1585421514738-01798e348b17?w=400'
}

# Get all products
cursor.execute("SELECT product_id, product_name, category FROM products")
products = cursor.fetchall()

print(f"Updating {len(products)} product images...")

# Update each product
for product_id, product_name, category in products:
    # Try to get specific product image first, then fall back to category image
    image_url = product_images.get(product_name, category_images.get(category, 'https://via.placeholder.com/400'))
    
    cursor.execute(
        "UPDATE products SET image_url = %s WHERE product_id = %s",
        (image_url, product_id)
    )

conn.commit()
print(f"✅ Updated {len(products)} products with better matching images!")

conn.close()
