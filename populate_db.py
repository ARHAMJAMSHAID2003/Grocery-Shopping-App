import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_api.settings')
django.setup()

from api.models import Products, Users, Stores, Locations
from django.contrib.auth.hashers import make_password

def populate_database():
    print("🔄 Populating database with sample data...")
    
    # Create a location
    location, _ = Locations.objects.get_or_create(
        location_id=1,
        defaults={
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'zip_code': 400001,
            'address': 'Andheri West',
            'region': 'Western'
        }
    )
    print("✅ Location created")
    
    # Create a store
    store, _ = Stores.objects.get_or_create(
        store_id=1,
        defaults={
            'store_name': 'FreshMart Main Store',
            'location_id': 1,
            'manager_name': 'Rajesh Kumar',
            'phone': '9876543210',
            'email': 'freshmart@example.com',
            'opening_hours': '8:00 AM - 10:00 PM'
        }
    )
    print("✅ Store created")
    
    # Create a test user
    user, created = Users.objects.get_or_create(
        email='test@example.com',
        defaults={
            'name': 'Test User',
            'password_hash': make_password('password123'),
            'phone': '9876543210',
            'gender': 'Male',
            'age': 25,
            'location_id': 1,
            'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    if created:
        print(f"✅ Test user created - Email: test@example.com, Password: password123")
    else:
        print(f"ℹ️  Test user already exists")
    
    # Sample products with images
    products = [
        {
            'product_name': 'Fresh Tomatoes',
            'description': 'Fresh red tomatoes, perfect for salads and cooking',
            'category': 'Vegetables',
            'price': 40.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1546470427-227e9df5b001?w=400'
        },
        {
            'product_name': 'Whole Wheat Bread',
            'description': 'Healthy whole wheat bread, freshly baked',
            'category': 'Bakery',
            'price': 45.0,
            'stock_quantity': 50,
            'unit': 'loaf',
            'brand': 'Harvest Gold',
            'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
        },
        {
            'product_name': 'Full Cream Milk',
            'description': 'Fresh full cream milk, 1 liter pack',
            'category': 'Dairy',
            'price': 60.0,
            'stock_quantity': 80,
            'unit': 'liter',
            'brand': 'Amul',
            'image_url': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400'
        },
        {
            'product_name': 'Basmati Rice Premium',
            'description': 'Premium quality basmati rice, aromatic long grain',
            'category': 'Grains',
            'price': 150.0,
            'stock_quantity': 200,
            'unit': 'kg',
            'brand': 'India Gate',
            'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400'
        },
        {
            'product_name': 'Farm Fresh Eggs',
            'description': 'Fresh brown eggs, pack of 12',
            'category': 'Dairy',
            'price': 75.0,
            'stock_quantity': 60,
            'unit': 'dozen',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400'
        },
        {
            'product_name': 'Fresh Potatoes',
            'description': 'Fresh potatoes, ideal for all types of cooking',
            'category': 'Vegetables',
            'price': 30.0,
            'stock_quantity': 150,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400'
        },
        {
            'product_name': 'Red Onions',
            'description': 'Fresh red onions, premium quality',
            'category': 'Vegetables',
            'price': 35.0,
            'stock_quantity': 120,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1508747703725-719777637510?w=400'
        },
        {
            'product_name': 'Green Capsicum',
            'description': 'Fresh green bell peppers',
            'category': 'Vegetables',
            'price': 50.0,
            'stock_quantity': 40,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400'
        },
        {
            'product_name': 'Fresh Carrots',
            'description': 'Crunchy fresh carrots, rich in vitamins',
            'category': 'Vegetables',
            'price': 45.0,
            'stock_quantity': 90,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400'
        },
        {
            'product_name': 'Tata Salt',
            'description': 'Iodized table salt, 1kg pack',
            'category': 'Spices & Condiments',
            'price': 22.0,
            'stock_quantity': 200,
            'unit': 'kg',
            'brand': 'Tata',
            'image_url': 'https://images.unsplash.com/photo-1598349326066-91b5de6c2933?w=400'
        },
        {
            'product_name': 'Fortune Sunflower Oil',
            'description': 'Refined sunflower oil, 1 liter',
            'category': 'Cooking Oil',
            'price': 140.0,
            'stock_quantity': 75,
            'unit': 'liter',
            'brand': 'Fortune',
            'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400'
        },
        {
            'product_name': 'Amul Butter',
            'description': 'Fresh creamy butter, 500g pack',
            'category': 'Dairy',
            'price': 250.0,
            'stock_quantity': 45,
            'unit': 'pack',
            'brand': 'Amul',
            'image_url': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400'
        },
        {
            'product_name': 'Britannia Biscuits',
            'description': 'Marie Gold biscuits, family pack',
            'category': 'Snacks',
            'price': 45.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Britannia',
            'image_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400'
        },
        {
            'product_name': 'Fresh Apples',
            'description': 'Premium Kashmir apples',
            'category': 'Fruits',
            'price': 180.0,
            'stock_quantity': 70,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400'
        },
        {
            'product_name': 'Fresh Bananas',
            'description': 'Ripe yellow bananas',
            'category': 'Fruits',
            'price': 50.0,
            'stock_quantity': 80,
            'unit': 'dozen',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400'
        },
        {
            'product_name': 'Green Tea',
            'description': 'Organic green tea, 100 bags',
            'category': 'Beverages',
            'price': 200.0,
            'stock_quantity': 50,
            'unit': 'pack',
            'brand': 'Lipton',
            'image_url': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400'
        },
        {
            'product_name': 'Fresh Coriander',
            'description': 'Fresh coriander leaves bundle',
            'category': 'Vegetables',
            'price': 20.0,
            'stock_quantity': 60,
            'unit': 'bundle',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1607167322256-b6e6c35367b0?w=400'
        },
        {
            'product_name': 'Maggi Noodles',
            'description': '2-minute instant noodles, pack of 12',
            'category': 'Instant Food',
            'price': 144.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Maggi',
            'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400'
        },
        {
            'product_name': 'Coca Cola',
            'description': 'Coca Cola soft drink, 2 liter bottle',
            'category': 'Beverages',
            'price': 90.0,
            'stock_quantity': 60,
            'unit': 'bottle',
            'brand': 'Coca Cola',
            'image_url': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=400'
        },
        {
            'product_name': 'Colgate Toothpaste',
            'description': 'Colgate total advanced health, 200g',
            'category': 'Personal Care',
            'price': 120.0,
            'stock_quantity': 80,
            'unit': 'tube',
            'brand': 'Colgate',
            'image_url': 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'
        },
    ]
    
    created_count = 0
    for product_data in products:
        product, created = Products.objects.get_or_create(
            product_name=product_data['product_name'],
            defaults={
                **product_data,
                'store_id': 1
            }
        )
        if created:
            created_count += 1
            print(f"✅ Added: {product_data['product_name']}")
        else:
            print(f"ℹ️  Already exists: {product_data['product_name']}")
    
    total_products = Products.objects.count()
    print(f"\n🎉 Database populated successfully!")
    print(f"📦 Total products: {total_products}")
    print(f"➕ New products added: {created_count}")
    print(f"\n👤 Test Login Credentials:")
    print(f"   Email: test@example.com")
    print(f"   Password: password123")

if __name__ == '__main__':
    populate_database()
