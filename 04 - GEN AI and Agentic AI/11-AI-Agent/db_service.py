import mysql.connector as mysql
from contextlib import closing


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "ecommerce"
}


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return mysql.connect(**DB_CONFIG)


# ==========================================
# GET ORDER STATUS
# ==========================================

def get_order_status(order_id):
    query = """
        SELECT order_id, customer_name, product_name, order_status
        FROM orders
        WHERE order_id = %s
    """

    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:

            cursor.execute(query, (order_id,))
            order = cursor.fetchone()

            if not order:
                return "Order Not Found"

            return {
                "order_id": order[0],
                "customer_name": order[1],
                "product_name": order[2],
                "status": order[3]
            }


# ==========================================
# CANCEL ORDER
# ==========================================

def cancel_order(order_id):
    select_query = """
        SELECT order_status
        FROM orders
        WHERE order_id = %s
    """

    update_query = """
        UPDATE orders
        SET order_status = 'CANCELLED'
        WHERE order_id = %s
    """

    with closing(get_connection()) as connection:
        with closing(connection.cursor()) as cursor:

            # Get current order status
            cursor.execute(select_query, (order_id,))
            order = cursor.fetchone()

            if not order:
                return "Order Not Found"

            status = order[0]

            # Validate order status
            if status == "DELIVERED":
                return "Order cannot be cancelled because it is already delivered"

            if status == "CANCELLED":
                return "Order is already cancelled"

            # Cancel order
            cursor.execute(update_query, (order_id,))
            connection.commit()

            return "Order Cancelled Successfully"
