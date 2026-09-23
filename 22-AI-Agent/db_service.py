import mysql.connector as mysql


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "ecommerce"
}


# ==========================================
# GET ORDER STATUS
# ==========================================

def get_order_status(order_id):
    connection = mysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT order_id, customer_name, product_name, order_status
        FROM orders
        WHERE order_id = %s
    """, (order_id,))

    order = cursor.fetchone()

    cursor.close()
    connection.close()

    if order is None:
        return "Order Not Found"

    return {
        "order_id": order[0],
        "customer_name": order[1],
        "product_name": order[2],
        "status" : order[3]
    }


# ==========================================
# CANCEL ORDER
# ==========================================

def cancel_order(order_id):
    connection = mysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT order_status
                   FROM orders
                   WHERE order_id = %s
                   """, (order_id,))
    order = cursor.fetchone()

    if order is None:
        cursor.close()
        connection.close()
        return "Order Not Found"

    status = order[0]

    if status == "DELIVERED":
        cursor.close()
        connection.close()
        return "Order cannot be cancelled because it is already delivered"

    if status == "CANCELLED":
        cursor.close()
        connection.close()
        return "Order is already cancelled"

    cursor.execute("""
                   UPDATE orders
                   SET order_status = 'CANCELLED'
                   WHERE order_id = %s
                   """, (order_id,))

    connection.commit()
    cursor.close()
    connection.close()

    return "Order Cancelled Successfully"