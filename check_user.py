import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_api.settings')
django.setup()

from api.models import Users
from django.contrib.auth.hashers import make_password, check_password

# Check if user exists
try:
    user = Users.objects.get(email='test@example.com')
    print(f"✅ User found!")
    print(f"   User ID: {user.user_id}")
    print(f"   Name: {user.name}")
    print(f"   Email: {user.email}")
    
    # Update registration_date if missing
    if not user.registration_date:
        user.registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user.save()
        print(f"✅ Added registration date")
    
    # Test password
    test_password = 'password123'
    if check_password(test_password, user.password_hash):
        print(f"✅ Password is correct!")
    else:
        print(f"❌ Password doesn't match. Resetting...")
        user.password_hash = make_password('password123')
        user.save()
        print(f"✅ Password reset to: password123")
        
except Users.DoesNotExist:
    print("❌ User not found. Creating new user...")
    user = Users.objects.create(
        name='Test User',
        email='test@example.com',
        password_hash=make_password('password123'),
        phone='9876543210',
        gender='Male',
        age=25,
        location_id=1,
        registration_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    print(f"✅ User created!")
    print(f"   Email: test@example.com")
    print(f"   Password: password123")

print("\n🔐 Login Credentials:")
print("   Email: test@example.com")
print("   Password: password123")
