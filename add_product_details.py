import pymysql

# Connect to database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='111222333',
    database='grocery_db'
)
cursor = conn.cursor()

# Category-based descriptions and images
product_data = {
    'Fruits': {
        'desc': 'Fresh and nutritious fruit, perfect for snacking or cooking.',
        'image': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400'
    },
    'Dairy': {
        'desc': 'High-quality dairy product, rich in calcium and protein.',
        'image': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400'
    },
    'Bakery': {
        'desc': 'Freshly baked item, soft and delicious.',
        'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
    },
    'Meat': {
        'desc': 'Premium quality meat, carefully selected and prepared.',
        'image': 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400'
    },
    'Seafood': {
        'desc': 'Fresh seafood, sustainably sourced and delicious.',
        'image': 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=400'
    },
    'Vegetables': {
        'desc': 'Farm-fresh vegetables, packed with vitamins and nutrients.',
        'image': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400'
    },
    'Snacks': {
        'desc': 'Tasty snack perfect for any time of day.',
        'image': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=400'
    },
    'Beverages': {
        'desc': 'Refreshing beverage to quench your thirst.',
        'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400'
    },
    'Pantry': {
        'desc': 'Essential pantry staple for everyday cooking.',
        'image': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400'
    },
    'Frozen': {
        'desc': 'Convenient frozen item, ready when you need it.',
        'image': 'https://images.unsplash.com/photo-1628028811775-7c8e67db5eec?w=400'
    },
    'Household': {
        'desc': 'Essential household item for everyday needs.',
        'image': 'https://images.unsplash.com/photo-1585421514738-01798e348b17?w=400'
    }
}

# Get all products
cursor.execute("SELECT product_id, category FROM products")
products = cursor.fetchall()

print(f"Updating {len(products)} products...")

# Update each product
for product_id, category in products:
    # Get description and image based on category
    cat_data = product_data.get(category, {
        'desc': 'Quality product available at great prices.',
        'image': 'https://images.unsplash.com/photo-1534723328310-e82dad3ee43f?w=400'
    })
    
    cursor.execute(
        "UPDATE products SET description = %s, image_url = %s WHERE product_id = %s",
        (cat_data['desc'], cat_data['image'], product_id)
    )

conn.commit()
print(f"✅ Updated {len(products)} products with descriptions and images!")

# Verify
cursor.execute("SELECT COUNT(*) FROM products WHERE description IS NOT NULL AND image_url IS NOT NULL")
count = cursor.fetchone()[0]
print(f"✅ {count} products now have complete data")

conn.close()
