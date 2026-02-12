import pymysql

print("Fixing MySQL tables for CRUD operations...")

connection = pymysql.connect(
    host="localhost", user="root", password="111222333", database="grocery_db"
)

cursor = connection.cursor()

# Modify existing tables to add AUTO_INCREMENT and proper keys
queries = [
    # Users table
    "ALTER TABLE users MODIFY user_id INT AUTO_INCREMENT PRIMARY KEY",
    "ALTER TABLE users ADD COLUMN password_hash VARCHAR(255) AFTER email",
    # Products table - already has store_id FK
    "ALTER TABLE products MODIFY product_id INT AUTO_INCREMENT PRIMARY KEY",
    "ALTER TABLE products ADD COLUMN image_url VARCHAR(500) AFTER brand",
    "ALTER TABLE products ADD COLUMN description TEXT AFTER product_name",
    # Stores table
    "ALTER TABLE stores MODIFY store_id INT AUTO_INCREMENT PRIMARY KEY",
    # Locations table
    "ALTER TABLE locations MODIFY location_id INT AUTO_INCREMENT PRIMARY KEY",
    # Orders table
    "ALTER TABLE orders MODIFY order_id INT AUTO_INCREMENT PRIMARY KEY",
    # Order items table
    "ALTER TABLE order_items MODIFY order_item_id INT AUTO_INCREMENT PRIMARY KEY",
    # Create cart table
    """
    CREATE TABLE IF NOT EXISTS cart (
        cart_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
    )
    """,
]

for query in queries:
    try:
        cursor.execute(query)
        connection.commit()
        print(f"✓ Executed: {query[:60]}...")
    except Exception as e:
        print(f"✗ Error on: {query[:60]}...")
        print(f"  {str(e)}")
        continue

print("\n" + "=" * 60)
print("✓ Tables updated for CRUD operations!")
print("=" * 60)

cursor.close()
connection.close()
