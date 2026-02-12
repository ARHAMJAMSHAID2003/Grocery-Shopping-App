import pymysql

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='111222333',
    database='grocery_db'
)

cursor = conn.cursor()

print("Enforcing NOT NULL constraints on critical fields...")

# Products table
print("\nUpdating products table...")
cursor.execute("ALTER TABLE products MODIFY product_name TEXT NOT NULL")
cursor.execute("ALTER TABLE products MODIFY price FLOAT NOT NULL")

# Users table
print("Updating users table...")
cursor.execute("ALTER TABLE users MODIFY name TEXT NOT NULL")
cursor.execute("ALTER TABLE users MODIFY email TEXT NOT NULL")

# Orders table
print("Updating orders table...")
cursor.execute("ALTER TABLE orders MODIFY user_id BIGINT NOT NULL")
cursor.execute("ALTER TABLE orders MODIFY order_date TEXT NOT NULL")
cursor.execute("ALTER TABLE orders MODIFY total_amount FLOAT NOT NULL")
cursor.execute("ALTER TABLE orders MODIFY status TEXT NOT NULL")

# OrderItems table
print("Updating order_items table...")
cursor.execute("ALTER TABLE order_items MODIFY order_id BIGINT NOT NULL")
cursor.execute("ALTER TABLE order_items MODIFY product_id BIGINT NOT NULL")
cursor.execute("ALTER TABLE order_items MODIFY quantity BIGINT NOT NULL")
cursor.execute("ALTER TABLE order_items MODIFY unit_price FLOAT NOT NULL")

# Cart table (already has NOT NULL on quantity, user_id, product_id via ForeignKey)
print("Updating cart table...")
cursor.execute("ALTER TABLE cart MODIFY quantity INT NOT NULL")

# Stores table
print("Updating stores table...")
cursor.execute("ALTER TABLE stores MODIFY store_name TEXT NOT NULL")
cursor.execute("ALTER TABLE stores MODIFY location_id BIGINT NOT NULL")

# Locations table
print("Updating locations table...")
cursor.execute("ALTER TABLE locations MODIFY city TEXT NOT NULL")
cursor.execute("ALTER TABLE locations MODIFY state TEXT NOT NULL")

conn.commit()
print("\n✓ All NOT NULL constraints applied successfully!")

cursor.close()
conn.close()
