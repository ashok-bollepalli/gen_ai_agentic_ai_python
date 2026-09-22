import sqlite3

# Database name
DB_NAME = "orders.db"


# ==========================================
# 1. CREATE DATABASE AND TABLE
# ==========================================

def create_database():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            product_name TEXT,
            order_status TEXT
        )
    """)

    # Sample orders
    cursor.execute("""
        INSERT OR IGNORE INTO orders
        VALUES ('ORD1001', 'Rahul', 'iPhone 17', 'SHIPPED')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO orders
        VALUES ('ORD1002', 'Priya', 'Samsung Galaxy S26', 'DELIVERED')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO orders
        VALUES ('ORD1003', 'Arun', 'Sony Headphones', 'PROCESSING')
    """)

    connection.commit()
    connection.close()


# ==========================================
# 2. GET ORDER STATUS
# ==========================================

def get_order_status(order_id):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, customer_name, product_name, order_status
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return "Order not found"

    return {
        "order_id": order[0],
        "customer_name": order[1],
        "product_name": order[2],
        "status": order[3]
    }


# ==========================================
# 3. CANCEL ORDER
# ==========================================

def cancel_order(order_id):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    # Check current status
    cursor.execute("""
        SELECT order_status
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    if order is None:
        connection.close()
        return "Order not found"

    status = order[0]

    # Already delivered
    if status == "DELIVERED":
        connection.close()
        return "Order cannot be cancelled because it is already delivered"

    # Already cancelled
    if status == "CANCELLED":
        connection.close()
        return "Order is already cancelled"

    # Cancel order
    cursor.execute("""
        UPDATE orders
        SET order_status = 'CANCELLED'
        WHERE order_id = ?
    """, (order_id,))

    connection.commit()
    connection.close()

    return "Order cancelled successfully"


# ==========================================
# 4. MAIN
# ==========================================

if __name__ == "__main__":

    # Create database
    create_database()

    print("\n===== ORDER MANAGEMENT DEMO =====")

    # Get order status
    print("\nOrder Status:")
    print(get_order_status("ORD1001"))

    # Cancel order
    print("\nCancel Order:")
    print(cancel_order("ORD1003"))

    # Check status again
    print("\nOrder Status After Cancellation:")
    print(get_order_status("ORD1003"))