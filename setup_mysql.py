import pymysql
import sys

print("=" * 60)
print("MYSQL CONNECTION TEST")
print("=" * 60)

print("\nEnter your MySQL root password:")
password = input("Password: ")

try:
    # Test connection
    print("\nTesting MySQL connection...")
    connection = pymysql.connect(host="localhost", user="root", password=password)
    print("✓ MySQL connection successful!")

    # Create database
    print("Creating grocery_db database...")
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS grocery_db")
    cursor.execute("CREATE DATABASE grocery_db")
    print("✓ Database created!")

    cursor.close()
    connection.close()

    print("\n" + "=" * 60)
    print("✓ READY! Now run: python load_to_mysql.py")
    print("=" * 60)

except pymysql.err.OperationalError as e:
    print(f"\n✗ ERROR: {e}")
    print("\nPossible issues:")
    print("1. MySQL service not running - Start it from Services or MySQL Workbench")
    print("2. Wrong password")
    print("3. MySQL not installed properly")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    sys.exit(1)
