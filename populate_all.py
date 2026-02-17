import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_api.settings')
django.setup()

from api.models import Products, Users, Stores, Locations, Cart, OrderItems
from django.contrib.auth.hashers import make_password
from datetime import datetime

def populate_database():
    print("🔄 Populating database with all products...")
    
    # Ensure location exists
    location, _ = Locations.objects.get_or_create(
        location_id=1,
        defaults={
            'city': 'Lahore',
            'state': 'Punjab',
            'zip_code': 54000,
            'address': 'Gulberg III',
            'region': 'Central'
        }
    )
    
    # Ensure store exists
    store, _ = Stores.objects.get_or_create(
        store_id=1,
        defaults={
            'store_name': 'FreshMart Main Store',
            'location_id': 1,
            'manager_name': 'Ahmed Khan',
            'phone': '03001234567',
            'email': 'freshmart@example.com',
            'opening_hours': '8:00 AM - 11:00 PM'
        }
    )
    
    # Ensure test user exists
    user, created = Users.objects.get_or_create(
        email='test@example.com',
        defaults={
            'name': 'Test User',
            'password_hash': make_password('password123'),
            'phone': '03001234567',
            'gender': 'Male',
            'age': 25,
            'location_id': 1,
            'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
    products = [
        # ==================== VEGETABLES ====================
        {
            'product_name': 'Fresh Tomatoes',
            'description': 'Tamatar - Fresh red tomatoes for cooking and salads',
            'category': 'Vegetables',
            'price': 120.0,
            'stock_quantity': 200,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1546470427-227e9df5b001?w=400'
        },
        {
            'product_name': 'Potatoes',
            'description': 'Aloo - Fresh potatoes for every dish',
            'category': 'Vegetables',
            'price': 80.0,
            'stock_quantity': 300,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400'
        },
        {
            'product_name': 'Red Onions',
            'description': 'Pyaaz - Fresh red onions, essential for cooking',
            'category': 'Vegetables',
            'price': 150.0,
            'stock_quantity': 250,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1508747703725-719777637510?w=400'
        },
        {
            'product_name': 'Green Chillies',
            'description': 'Hari Mirch - Fresh green chillies for spicy dishes',
            'category': 'Vegetables',
            'price': 100.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=400'
        },
        {
            'product_name': 'Fresh Ginger',
            'description': 'Adrak - Essential spice for cooking and tea',
            'category': 'Vegetables',
            'price': 250.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=400'
        },
        {
            'product_name': 'Garlic',
            'description': 'Lehsun - Fresh garlic bulbs for cooking',
            'category': 'Vegetables',
            'price': 300.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1540148426945-6cf22a6b2571?w=400'
        },
        {
            'product_name': 'Fresh Carrots',
            'description': 'Gajar - Crunchy orange carrots rich in vitamins',
            'category': 'Vegetables',
            'price': 90.0,
            'stock_quantity': 150,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400'
        },
        {
            'product_name': 'Green Capsicum',
            'description': 'Shimla Mirch - Fresh green bell peppers',
            'category': 'Vegetables',
            'price': 180.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400'
        },
        {
            'product_name': 'Fresh Coriander',
            'description': 'Hara Dhania - Fresh coriander leaves bundle',
            'category': 'Vegetables',
            'price': 30.0,
            'stock_quantity': 120,
            'unit': 'bundle',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1607167322256-b6e6c35367b0?w=400'
        },
        {
            'product_name': 'Fresh Mint',
            'description': 'Pudina - Fresh mint leaves for raita and chutney',
            'category': 'Vegetables',
            'price': 30.0,
            'stock_quantity': 100,
            'unit': 'bundle',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1628556270448-4d4e4148e1b1?w=400'
        },
        {
            'product_name': 'Spinach',
            'description': 'Palak - Fresh spinach leaves for saag',
            'category': 'Vegetables',
            'price': 40.0,
            'stock_quantity': 100,
            'unit': 'bundle',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400'
        },
        {
            'product_name': 'Cabbage',
            'description': 'Band Gobhi - Fresh green cabbage',
            'category': 'Vegetables',
            'price': 60.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400'
        },
        {
            'product_name': 'Cauliflower',
            'description': 'Phool Gobhi - Fresh white cauliflower',
            'category': 'Vegetables',
            'price': 100.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=400'
        },
        {
            'product_name': 'Cucumber',
            'description': 'Kheera - Fresh cucumbers for salad',
            'category': 'Vegetables',
            'price': 80.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=400'
        },
        {
            'product_name': 'Lemon',
            'description': 'Nimbu - Fresh lemons for juice and cooking',
            'category': 'Vegetables',
            'price': 200.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1590502593747-42a996133562?w=400'
        },
        {
            'product_name': 'Bitter Gourd',
            'description': 'Karela - Fresh bitter gourd for healthy cooking',
            'category': 'Vegetables',
            'price': 120.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1604322173498-fa69c27e0fa7?w=400'
        },
        {
            'product_name': 'Okra',
            'description': 'Bhindi - Fresh ladyfinger for frying and curry',
            'category': 'Vegetables',
            'price': 140.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1425543103986-22abb7d7e8d2?w=400'
        },
        {
            'product_name': 'Peas',
            'description': 'Matar - Fresh green peas',
            'category': 'Vegetables',
            'price': 160.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=400'
        },
        {
            'product_name': 'Radish',
            'description': 'Mooli - Fresh white radish',
            'category': 'Vegetables',
            'price': 60.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1447175008436-054170c2e979?w=400'
        },
        {
            'product_name': 'Turnip',
            'description': 'Shalgam - Fresh turnips for winter cooking',
            'category': 'Vegetables',
            'price': 70.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1594282486756-075b73ecab1b?w=400'
        },

        # ==================== FRUITS ====================
        {
            'product_name': 'Fresh Bananas',
            'description': 'Kela - Ripe yellow bananas, perfect snack',
            'category': 'Fruits',
            'price': 120.0,
            'stock_quantity': 150,
            'unit': 'dozen',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400'
        },
        {
            'product_name': 'Fresh Apples',
            'description': 'Seb - Premium quality red apples',
            'category': 'Fruits',
            'price': 350.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Kashmir Fresh',
            'image_url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400'
        },
        {
            'product_name': 'Mangoes',
            'description': 'Aam - Sweet and juicy mangoes',
            'category': 'Fruits',
            'price': 400.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400'
        },
        {
            'product_name': 'Oranges',
            'description': 'Santra/Malta - Fresh juicy oranges',
            'category': 'Fruits',
            'price': 250.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1547514701-42782101795e?w=400'
        },
        {
            'product_name': 'Grapes',
            'description': 'Angoor - Fresh seedless grapes',
            'category': 'Fruits',
            'price': 300.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400'
        },
        {
            'product_name': 'Watermelon',
            'description': 'Tarbooz - Fresh sweet watermelon',
            'category': 'Fruits',
            'price': 60.0,
            'stock_quantity': 50,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1563114773-84221bd62daa?w=400'
        },
        {
            'product_name': 'Pomegranate',
            'description': 'Anaar - Fresh ruby red pomegranate',
            'category': 'Fruits',
            'price': 400.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400'
        },
        {
            'product_name': 'Guava',
            'description': 'Amrood - Fresh guava, sweet and crunchy',
            'category': 'Fruits',
            'price': 150.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=400'
        },
        {
            'product_name': 'Papaya',
            'description': 'Papeeta - Fresh ripe papaya',
            'category': 'Fruits',
            'price': 120.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=400'
        },
        {
            'product_name': 'Strawberries',
            'description': 'Fresh red strawberries',
            'category': 'Fruits',
            'price': 500.0,
            'stock_quantity': 40,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400'
        },

        # ==================== DAIRY ====================
        {
            'product_name': 'Full Cream Milk',
            'description': 'Doodh - Fresh full cream milk',
            'category': 'Dairy',
            'price': 220.0,
            'stock_quantity': 200,
            'unit': 'liter',
            'brand': 'Olpers',
            'image_url': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400'
        },
        {
            'product_name': 'Yogurt',
            'description': 'Dahi - Fresh creamy yogurt',
            'category': 'Dairy',
            'price': 130.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Nurpur',
            'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400'
        },
        {
            'product_name': 'Butter',
            'description': 'Makhan - Fresh creamy butter',
            'category': 'Dairy',
            'price': 450.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Lurpak',
            'image_url': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400'
        },
        {
            'product_name': 'Cheese Slices',
            'description': 'Cheese - Processed cheese slices',
            'category': 'Dairy',
            'price': 350.0,
            'stock_quantity': 60,
            'unit': 'pack',
            'brand': 'Adams',
            'image_url': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400'
        },
        {
            'product_name': 'Cream',
            'description': 'Fresh cream for cooking and desserts',
            'category': 'Dairy',
            'price': 180.0,
            'stock_quantity': 60,
            'unit': 'pack',
            'brand': 'Olpers',
            'image_url': 'https://images.unsplash.com/photo-1625869737004-4fc9e97bf01b?w=400'
        },
        {
            'product_name': 'Farm Fresh Eggs',
            'description': 'Ande - Fresh brown eggs pack of 12',
            'category': 'Dairy',
            'price': 300.0,
            'stock_quantity': 100,
            'unit': 'dozen',
            'brand': 'SB Eggs',
            'image_url': 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400'
        },
        {
            'product_name': 'Raita Mix Yogurt',
            'description': 'Raita wala dahi - Yogurt perfect for raita',
            'category': 'Dairy',
            'price': 100.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Nurpur',
            'image_url': 'https://images.unsplash.com/photo-1571212515416-fef01fc43637?w=400'
        },

        # ==================== MEAT & POULTRY ====================
        {
            'product_name': 'Chicken Whole',
            'description': 'Murghi - Fresh whole chicken',
            'category': 'Meat',
            'price': 450.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'K&Ns',
            'image_url': 'https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=400'
        },
        {
            'product_name': 'Chicken Breast',
            'description': 'Boneless chicken breast fillets',
            'category': 'Meat',
            'price': 650.0,
            'stock_quantity': 50,
            'unit': 'kg',
            'brand': 'K&Ns',
            'image_url': 'https://images.unsplash.com/photo-1604503468506-a8da13d82571?w=400'
        },
        {
            'product_name': 'Mutton',
            'description': 'Bakra Gosht - Fresh mutton with bone',
            'category': 'Meat',
            'price': 1800.0,
            'stock_quantity': 40,
            'unit': 'kg',
            'brand': 'Meat One',
            'image_url': 'https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=400'
        },
        {
            'product_name': 'Beef',
            'description': 'Gaye ka Gosht - Fresh beef cuts',
            'category': 'Meat',
            'price': 1200.0,
            'stock_quantity': 50,
            'unit': 'kg',
            'brand': 'Meat One',
            'image_url': 'https://images.unsplash.com/photo-1588347818036-558601350947?w=400'
        },
        {
            'product_name': 'Chicken Nuggets',
            'description': 'Frozen crispy chicken nuggets',
            'category': 'Meat',
            'price': 550.0,
            'stock_quantity': 40,
            'unit': 'pack',
            'brand': 'K&Ns',
            'image_url': 'https://images.unsplash.com/photo-1562967914-608f82629710?w=400'
        },
        {
            'product_name': 'Seekh Kabab',
            'description': 'Frozen seekh kabab ready to cook',
            'category': 'Meat',
            'price': 700.0,
            'stock_quantity': 40,
            'unit': 'pack',
            'brand': 'K&Ns',
            'image_url': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400'
        },
        {
            'product_name': 'Chicken Keema',
            'description': 'Qeema - Minced chicken meat',
            'category': 'Meat',
            'price': 550.0,
            'stock_quantity': 50,
            'unit': 'kg',
            'brand': 'Meat One',
            'image_url': 'https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=400'
        },

        # ==================== GRAINS & STAPLES ====================
        {
            'product_name': 'Basmati Rice',
            'description': 'Chawal - Premium basmati rice, long grain aromatic',
            'category': 'Pantry',
            'price': 350.0,
            'stock_quantity': 200,
            'unit': 'kg',
            'brand': 'Guard',
            'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400'
        },
        {
            'product_name': 'Wheat Flour',
            'description': 'Atta - Chakki fresh whole wheat flour',
            'category': 'Pantry',
            'price': 140.0,
            'stock_quantity': 200,
            'unit': 'kg',
            'brand': 'Sunridge',
            'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400'
        },
        {
            'product_name': 'Sugar',
            'description': 'Cheeni - Refined white sugar',
            'category': 'Pantry',
            'price': 150.0,
            'stock_quantity': 200,
            'unit': 'kg',
            'brand': 'Al-Moiz',
            'image_url': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=400'
        },
        {
            'product_name': 'Salt',
            'description': 'Namak - Iodized table salt',
            'category': 'Pantry',
            'price': 60.0,
            'stock_quantity': 300,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1598349326066-91b5de6c2933?w=400'
        },
        {
            'product_name': 'Daal Chana',
            'description': 'Chana Daal - Split chickpea lentils',
            'category': 'Pantry',
            'price': 280.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1613758947307-f3b8f5d80711?w=400'
        },
        {
            'product_name': 'Daal Masoor',
            'description': 'Masoor ki Daal - Red lentils',
            'category': 'Pantry',
            'price': 320.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1613758947307-f3b8f5d80711?w=400'
        },
        {
            'product_name': 'Daal Moong',
            'description': 'Moong ki Daal - Split mung bean lentils',
            'category': 'Pantry',
            'price': 350.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1613758947307-f3b8f5d80711?w=400'
        },
        {
            'product_name': 'Chickpeas',
            'description': 'Chanay - White chickpeas for cholay',
            'category': 'Pantry',
            'price': 300.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1515543904413-63037da60ef5?w=400'
        },
        {
            'product_name': 'Maida',
            'description': 'All purpose white flour for naan and baking',
            'category': 'Pantry',
            'price': 120.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'Sunridge',
            'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400'
        },
        {
            'product_name': 'Besan',
            'description': 'Gram flour for pakoras and sweets',
            'category': 'Pantry',
            'price': 250.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400'
        },

        # ==================== COOKING OIL ====================
        {
            'product_name': 'Cooking Oil',
            'description': 'Khana Pakane ka Tel - Sunflower cooking oil',
            'category': 'Cooking Oil',
            'price': 550.0,
            'stock_quantity': 100,
            'unit': 'liter',
            'brand': 'Dalda',
            'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400'
        },
        {
            'product_name': 'Olive Oil',
            'description': 'Extra virgin olive oil for salads',
            'category': 'Cooking Oil',
            'price': 1200.0,
            'stock_quantity': 40,
            'unit': 'bottle',
            'brand': 'Borges',
            'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400'
        },
        {
            'product_name': 'Ghee',
            'description': 'Desi Ghee - Pure clarified butter',
            'category': 'Cooking Oil',
            'price': 1600.0,
            'stock_quantity': 50,
            'unit': 'kg',
            'brand': 'Nurpur',
            'image_url': 'https://images.unsplash.com/photo-1600398236373-76903f48a048?w=400'
        },

        # ==================== SPICES & CONDIMENTS ====================
        {
            'product_name': 'Red Chilli Powder',
            'description': 'Laal Mirch - Pure red chilli powder',
            'category': 'Spices & Condiments',
            'price': 500.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Turmeric Powder',
            'description': 'Haldi - Pure turmeric powder for cooking',
            'category': 'Spices & Condiments',
            'price': 450.0,
            'stock_quantity': 100,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400'
        },
        {
            'product_name': 'Cumin Seeds',
            'description': 'Zeera - Whole cumin seeds for tempering',
            'category': 'Spices & Condiments',
            'price': 600.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Shan',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Coriander Powder',
            'description': 'Dhania Powder - Ground coriander for curries',
            'category': 'Spices & Condiments',
            'price': 400.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Garam Masala',
            'description': 'Mixed spice blend for curries',
            'category': 'Spices & Condiments',
            'price': 700.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Shan',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Black Pepper',
            'description': 'Kali Mirch - Whole black peppercorns',
            'category': 'Spices & Condiments',
            'price': 800.0,
            'stock_quantity': 40,
            'unit': 'kg',
            'brand': 'Shan',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Biryani Masala',
            'description': 'Shan Biryani Masala mix',
            'category': 'Spices & Condiments',
            'price': 120.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Shan',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Nihari Masala',
            'description': 'Shan Nihari Masala mix for nihari',
            'category': 'Spices & Condiments',
            'price': 100.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Shan',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
        {
            'product_name': 'Vinegar',
            'description': 'Sirka - White vinegar for cooking',
            'category': 'Spices & Condiments',
            'price': 100.0,
            'stock_quantity': 80,
            'unit': 'bottle',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400'
        },
        {
            'product_name': 'Tomato Ketchup',
            'description': 'Tomato sauce for snacks and burgers',
            'category': 'Spices & Condiments',
            'price': 250.0,
            'stock_quantity': 80,
            'unit': 'bottle',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1598511757337-fe2cafc31ba0?w=400'
        },
        {
            'product_name': 'Soy Sauce',
            'description': 'Soy sauce for Chinese cooking',
            'category': 'Spices & Condiments',
            'price': 180.0,
            'stock_quantity': 60,
            'unit': 'bottle',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1598511757337-fe2cafc31ba0?w=400'
        },

        # ==================== BAKERY ====================
        {
            'product_name': 'White Bread',
            'description': 'Double Roti - Fresh white bread loaf',
            'category': 'Bakery',
            'price': 150.0,
            'stock_quantity': 80,
            'unit': 'loaf',
            'brand': 'Dawn',
            'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
        },
        {
            'product_name': 'Whole Wheat Bread',
            'description': 'Brown bread - Healthy whole wheat',
            'category': 'Bakery',
            'price': 180.0,
            'stock_quantity': 60,
            'unit': 'loaf',
            'brand': 'Dawn',
            'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
        },
        {
            'product_name': 'Naan',
            'description': 'Tandoori Naan - Fresh baked naan bread pack',
            'category': 'Bakery',
            'price': 80.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Local',
            'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'
        },
        {
            'product_name': 'Cake Rusk',
            'description': 'Cake Rusk for tea time',
            'category': 'Bakery',
            'price': 200.0,
            'stock_quantity': 60,
            'unit': 'pack',
            'brand': 'English',
            'image_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400'
        },
        {
            'product_name': 'Pita Bread',
            'description': 'Pita bread for shawarma and wraps',
            'category': 'Bakery',
            'price': 250.0,
            'stock_quantity': 40,
            'unit': 'pack',
            'brand': 'Dawn',
            'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
        },

        # ==================== BEVERAGES ====================
        {
            'product_name': 'Tapal Danedar Tea',
            'description': 'Chai Patti - Premium black tea leaves',
            'category': 'Beverages',
            'price': 350.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Tapal',
            'image_url': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400'
        },
        {
            'product_name': 'Green Tea',
            'description': 'Sabz Chai - Organic green tea bags',
            'category': 'Beverages',
            'price': 400.0,
            'stock_quantity': 60,
            'unit': 'pack',
            'brand': 'Lipton',
            'image_url': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400'
        },
        {
            'product_name': 'Coca Cola',
            'description': 'Coca Cola soft drink 1.5 liter',
            'category': 'Beverages',
            'price': 180.0,
            'stock_quantity': 100,
            'unit': 'bottle',
            'brand': 'Coca Cola',
            'image_url': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=400'
        },
        {
            'product_name': 'Pepsi',
            'description': 'Pepsi soft drink 1.5 liter',
            'category': 'Beverages',
            'price': 180.0,
            'stock_quantity': 100,
            'unit': 'bottle',
            'brand': 'Pepsi',
            'image_url': 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400'
        },
        {
            'product_name': 'Sprite',
            'description': 'Sprite lemon lime soda 1.5 liter',
            'category': 'Beverages',
            'price': 170.0,
            'stock_quantity': 80,
            'unit': 'bottle',
            'brand': 'Sprite',
            'image_url': 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400'
        },
        {
            'product_name': 'Mineral Water',
            'description': 'Pani - Nestle pure mineral water 1.5L',
            'category': 'Beverages',
            'price': 80.0,
            'stock_quantity': 200,
            'unit': 'bottle',
            'brand': 'Nestle',
            'image_url': 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400'
        },
        {
            'product_name': 'Mango Juice',
            'description': 'Aam ka Juice - Real mango juice pack',
            'category': 'Beverages',
            'price': 120.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Nestle',
            'image_url': 'https://images.unsplash.com/photo-1546173159-315724a31696?w=400'
        },
        {
            'product_name': 'Rooh Afza',
            'description': 'Rooh Afza sharbat syrup',
            'category': 'Beverages',
            'price': 350.0,
            'stock_quantity': 60,
            'unit': 'bottle',
            'brand': 'Hamdard',
            'image_url': 'https://images.unsplash.com/photo-1546173159-315724a31696?w=400'
        },

        # ==================== SNACKS ====================
        {
            'product_name': 'Lays Chips',
            'description': 'Lays classic salted chips',
            'category': 'Snacks',
            'price': 70.0,
            'stock_quantity': 120,
            'unit': 'pack',
            'brand': 'Lays',
            'image_url': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400'
        },
        {
            'product_name': 'Kurkure',
            'description': 'Kurkure crunchy masala snack',
            'category': 'Snacks',
            'price': 50.0,
            'stock_quantity': 120,
            'unit': 'pack',
            'brand': 'Kurkure',
            'image_url': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400'
        },
        {
            'product_name': 'Biscuits',
            'description': 'Chai ke saath Biscuit - Tea biscuits',
            'category': 'Snacks',
            'price': 80.0,
            'stock_quantity': 150,
            'unit': 'pack',
            'brand': 'Lu',
            'image_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400'
        },
        {
            'product_name': 'Nimko',
            'description': 'Namkeen - Traditional savory snack mix',
            'category': 'Snacks',
            'price': 150.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Kolson',
            'image_url': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400'
        },
        {
            'product_name': 'Chocolate',
            'description': 'Dairy Milk chocolate bar',
            'category': 'Snacks',
            'price': 200.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Cadbury',
            'image_url': 'https://images.unsplash.com/photo-1549007994-cb92caefdbd1?w=400'
        },
        {
            'product_name': 'Peanuts',
            'description': 'Moong Phali - Roasted salted peanuts',
            'category': 'Snacks',
            'price': 250.0,
            'stock_quantity': 60,
            'unit': 'kg',
            'brand': 'Farm Fresh',
            'image_url': 'https://images.unsplash.com/photo-1567892320421-1c657571ea4a?w=400'
        },
        {
            'product_name': 'Dates',
            'description': 'Khajoor - Premium Ajwa dates',
            'category': 'Snacks',
            'price': 800.0,
            'stock_quantity': 40,
            'unit': 'kg',
            'brand': 'Arabian',
            'image_url': 'https://images.unsplash.com/photo-1593904308879-e2f4a1e30a44?w=400'
        },
        {
            'product_name': 'Dry Fruits Mix',
            'description': 'Khushk Mewa - Mixed almonds, cashew, pistachio',
            'category': 'Snacks',
            'price': 2000.0,
            'stock_quantity': 30,
            'unit': 'kg',
            'brand': 'Premium',
            'image_url': 'https://images.unsplash.com/photo-1608797178974-15b35a64ede9?w=400'
        },

        # ==================== INSTANT FOOD ====================
        {
            'product_name': 'Maggi Noodles',
            'description': 'Instant noodles 2-minute ready',
            'category': 'Instant Food',
            'price': 50.0,
            'stock_quantity': 150,
            'unit': 'pack',
            'brand': 'Maggi',
            'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400'
        },
        {
            'product_name': 'Knorr Noodles',
            'description': 'Knorr chatpata instant noodles',
            'category': 'Instant Food',
            'price': 40.0,
            'stock_quantity': 150,
            'unit': 'pack',
            'brand': 'Knorr',
            'image_url': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400'
        },
        {
            'product_name': 'Pasta',
            'description': 'Macaroni pasta for cooking',
            'category': 'Instant Food',
            'price': 200.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Kolson',
            'image_url': 'https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=400'
        },
        {
            'product_name': 'Vermicelli',
            'description': 'Seviyan - Thin vermicelli for kheer',
            'category': 'Instant Food',
            'price': 80.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Kolson',
            'image_url': 'https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=400'
        },
        {
            'product_name': 'Cornflakes',
            'description': 'Breakfast cornflakes cereal',
            'category': 'Instant Food',
            'price': 450.0,
            'stock_quantity': 50,
            'unit': 'pack',
            'brand': 'Kelloggs',
            'image_url': 'https://images.unsplash.com/photo-1517456793572-1d8efd6dc135?w=400'
        },

        # ==================== FROZEN FOOD ====================
        {
            'product_name': 'Frozen Samosa',
            'description': 'Ready to fry samosas pack of 12',
            'category': 'Instant Food',
            'price': 350.0,
            'stock_quantity': 50,
            'unit': 'pack',
            'brand': 'K&Ns',
            'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400'
        },
        {
            'product_name': 'Frozen Parathas',
            'description': 'Ready to cook frozen parathas pack of 5',
            'category': 'Instant Food',
            'price': 280.0,
            'stock_quantity': 60,
            'unit': 'pack',
            'brand': 'Dawn',
            'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400'
        },
        {
            'product_name': 'French Fries',
            'description': 'Frozen french fries ready to fry',
            'category': 'Instant Food',
            'price': 350.0,
            'stock_quantity': 50,
            'unit': 'pack',
            'brand': 'McCain',
            'image_url': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400'
        },
        {
            'product_name': 'Ice Cream',
            'description': 'Vanilla ice cream family pack',
            'category': 'Instant Food',
            'price': 500.0,
            'stock_quantity': 40,
            'unit': 'tub',
            'brand': 'Walls',
            'image_url': 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=400'
        },

        # ==================== PERSONAL CARE ====================
        {
            'product_name': 'Toothpaste',
            'description': 'Colgate toothpaste for cavity protection',
            'category': 'Personal Care',
            'price': 200.0,
            'stock_quantity': 100,
            'unit': 'tube',
            'brand': 'Colgate',
            'image_url': 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400'
        },
        {
            'product_name': 'Shampoo',
            'description': 'Anti-dandruff shampoo 400ml',
            'category': 'Personal Care',
            'price': 550.0,
            'stock_quantity': 60,
            'unit': 'bottle',
            'brand': 'Head & Shoulders',
            'image_url': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400'
        },
        {
            'product_name': 'Soap',
            'description': 'Sabun - Bath soap bar pack of 3',
            'category': 'Personal Care',
            'price': 250.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'Lux',
            'image_url': 'https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=400'
        },
        {
            'product_name': 'Hand Wash',
            'description': 'Liquid hand wash antibacterial',
            'category': 'Personal Care',
            'price': 350.0,
            'stock_quantity': 80,
            'unit': 'bottle',
            'brand': 'Dettol',
            'image_url': 'https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=400'
        },
        {
            'product_name': 'Tissue Paper',
            'description': 'Tissue box 200 sheets',
            'category': 'Personal Care',
            'price': 150.0,
            'stock_quantity': 100,
            'unit': 'box',
            'brand': 'Rose Petal',
            'image_url': 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=400'
        },
        {
            'product_name': 'Toilet Paper',
            'description': 'Toilet roll pack of 4',
            'category': 'Personal Care',
            'price': 200.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Rose Petal',
            'image_url': 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=400'
        },

        # ==================== HOUSEHOLD ====================
        {
            'product_name': 'Dishwashing Liquid',
            'description': 'Bartan dhone ka liquid - Dish soap',
            'category': 'Personal Care',
            'price': 250.0,
            'stock_quantity': 80,
            'unit': 'bottle',
            'brand': 'Vim',
            'image_url': 'https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=400'
        },
        {
            'product_name': 'Laundry Detergent',
            'description': 'Surf Excel washing powder',
            'category': 'Personal Care',
            'price': 400.0,
            'stock_quantity': 80,
            'unit': 'kg',
            'brand': 'Surf Excel',
            'image_url': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400'
        },
        {
            'product_name': 'Floor Cleaner',
            'description': 'Surface floor cleaner liquid',
            'category': 'Personal Care',
            'price': 300.0,
            'stock_quantity': 60,
            'unit': 'bottle',
            'brand': 'Max',
            'image_url': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400'
        },
        {
            'product_name': 'Garbage Bags',
            'description': 'Black garbage bags pack of 30',
            'category': 'Personal Care',
            'price': 150.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'Generic',
            'image_url': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400'
        },
        {
            'product_name': 'Aluminium Foil',
            'description': 'Kitchen aluminium foil roll',
            'category': 'Personal Care',
            'price': 200.0,
            'stock_quantity': 60,
            'unit': 'roll',
            'brand': 'Generic',
            'image_url': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=400'
        },

        # ==================== BABY PRODUCTS ====================
        {
            'product_name': 'Baby Diapers',
            'description': 'Baby diapers medium size pack',
            'category': 'Personal Care',
            'price': 1200.0,
            'stock_quantity': 40,
            'unit': 'pack',
            'brand': 'Pampers',
            'image_url': 'https://images.unsplash.com/photo-1584839404428-1e8cc5e0e1c5?w=400'
        },
        {
            'product_name': 'Baby Milk Powder',
            'description': 'Infant formula milk powder',
            'category': 'Dairy',
            'price': 1800.0,
            'stock_quantity': 40,
            'unit': 'tin',
            'brand': 'Nestle',
            'image_url': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400'
        },

        # ==================== SEAFOOD ====================
        {
            'product_name': 'Fresh Fish',
            'description': 'Machli - Fresh fish fillets',
            'category': 'Seafood',
            'price': 800.0,
            'stock_quantity': 40,
            'unit': 'kg',
            'brand': 'Fresh Catch',
            'image_url': 'https://images.unsplash.com/photo-1544943910-a3ca1d29e9e2?w=400'
        },
        {
            'product_name': 'Prawns',
            'description': 'Jhingay - Fresh prawns cleaned',
            'category': 'Seafood',
            'price': 1500.0,
            'stock_quantity': 30,
            'unit': 'kg',
            'brand': 'Fresh Catch',
            'image_url': 'https://images.unsplash.com/photo-1565680018093-ebb6505020e4?w=400'
        },

        # ==================== EXTRAS ====================
        {
            'product_name': 'Honey',
            'description': 'Shahad - Pure natural honey',
            'category': 'Pantry',
            'price': 800.0,
            'stock_quantity': 40,
            'unit': 'jar',
            'brand': 'Marhaba',
            'image_url': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400'
        },
        {
            'product_name': 'Jam',
            'description': 'Mixed fruit jam for breakfast',
            'category': 'Pantry',
            'price': 300.0,
            'stock_quantity': 60,
            'unit': 'jar',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400'
        },
        {
            'product_name': 'Peanut Butter',
            'description': 'Creamy peanut butter spread',
            'category': 'Pantry',
            'price': 500.0,
            'stock_quantity': 40,
            'unit': 'jar',
            'brand': 'American Garden',
            'image_url': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400'
        },
        {
            'product_name': 'Mayonnaise',
            'description': 'Creamy mayonnaise for burgers and sandwiches',
            'category': 'Spices & Condiments',
            'price': 350.0,
            'stock_quantity': 60,
            'unit': 'jar',
            'brand': 'Young',
            'image_url': 'https://images.unsplash.com/photo-1598511757337-fe2cafc31ba0?w=400'
        },
        {
            'product_name': 'Pickles',
            'description': 'Achaar - Mixed pickle jar',
            'category': 'Spices & Condiments',
            'price': 250.0,
            'stock_quantity': 60,
            'unit': 'jar',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1598511757337-fe2cafc31ba0?w=400'
        },
        {
            'product_name': 'Condensed Milk',
            'description': 'Sweetened condensed milk for desserts',
            'category': 'Dairy',
            'price': 250.0,
            'stock_quantity': 60,
            'unit': 'tin',
            'brand': 'Nestle',
            'image_url': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400'
        },
        {
            'product_name': 'Baking Powder',
            'description': 'Baking powder for cakes and pastries',
            'category': 'Pantry',
            'price': 100.0,
            'stock_quantity': 80,
            'unit': 'pack',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400'
        },
        {
            'product_name': 'Food Color',
            'description': 'Food coloring set for cooking',
            'category': 'Pantry',
            'price': 50.0,
            'stock_quantity': 100,
            'unit': 'pack',
            'brand': 'National',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400'
        },
    ]
    
    # Clear dependent records first, then products
    OrderItems.objects.all().delete()
    Cart.objects.all().delete()
    Products.objects.all().delete()
    print("🗑️  Cleared old products (and related cart/order items)")
    
    created_count = 0
    for product_data in products:
        product = Products.objects.create(
            **product_data,
            store_id=1
        )
        created_count += 1
        print(f"  ✅ Added: {product_data['product_name']} ({product_data['category']})")
    
    total = Products.objects.count()
    print(f"\n🎉 Database populated successfully!")
    print(f"📦 Total products: {total}")
    print(f"➕ Products added: {created_count}")
    print(f"\n👤 Test Login: test@example.com / password123")

if __name__ == '__main__':
    populate_database()
