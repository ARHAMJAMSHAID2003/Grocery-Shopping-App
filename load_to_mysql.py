import pandas as pd
from sqlalchemy import create_engine, text
import warnings

warnings.filterwarnings("ignore")

print("=" * 60)
print("MYSQL DATA LOADER")
print("=" * 60)

# Get MySQL password
print("\nEnter your MySQL root password:")
print("(If you just installed MySQL, use the password you set during installation)")
password = input("Password: ")

# Read CSV files
print("\nReading CSV files...")
locations = pd.read_csv("locations.csv")
users = pd.read_csv("users.csv")
stores = pd.read_csv("stores.csv")
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")
order_items = pd.read_csv("order_items.csv")

# Connect to MySQL
print("Connecting to MySQL...")
try:
    # Connect directly to grocery_db (already created by setup_mysql.py)
    print("Connecting to grocery_db...")
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost/grocery_db")

    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.fetchone()[0]
        print(f"✓ Connected to database: {db_name}")

    # Load data
    print("\nLoading data to MySQL...")

    print("Loading LOCATIONS...")
    locations.to_sql(
        "locations", con=engine, if_exists="replace", index=False, chunksize=100
    )
    print(f"✓ LOCATIONS: {len(locations)} rows")

    print("Loading USERS...")
    users.to_sql("users", con=engine, if_exists="replace", index=False, chunksize=100)
    print(f"✓ USERS: {len(users)} rows")

    print("Loading STORES...")
    stores.to_sql("stores", con=engine, if_exists="replace", index=False, chunksize=100)
    print(f"✓ STORES: {len(stores)} rows")

    print("Loading PRODUCTS...")
    products.to_sql(
        "products", con=engine, if_exists="replace", index=False, chunksize=100
    )
    print(f"✓ PRODUCTS: {len(products)} rows")

    print("Loading ORDERS...")
    orders.to_sql("orders", con=engine, if_exists="replace", index=False, chunksize=100)
    print(f"✓ ORDERS: {len(orders)} rows")

    print("Loading ORDER_ITEMS...")
    order_items.to_sql(
        "order_items", con=engine, if_exists="replace", index=False, chunksize=100
    )
    print(f"✓ ORDER_ITEMS: {len(order_items)} rows")

    print("\n" + "=" * 60)
    print("✓ SUCCESS! ALL DATA LOADED TO MYSQL!")
    print("=" * 60)
    print("\nDatabase: grocery_db")
    print("Tables: locations, users, stores, products, orders, order_items")
    print("\nNow connect Power BI to MySQL:")
    print("  Server: localhost")
    print("  Database: grocery_db")
    print(f"  Username: root")
    print(f"  Password: {password}")

except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    print("\nMake sure:")
    print("1. MySQL is installed and running")
    print("2. Password is correct")
    print("3. Install pymysql: pip install pymysql")
