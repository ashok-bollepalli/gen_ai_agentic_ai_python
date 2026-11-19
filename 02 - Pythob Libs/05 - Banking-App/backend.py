
from db import get_connection


# Get all customers
def get_customers():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers ORDER BY id")

    customers = cursor.fetchall()

    conn.close()

    return customers


# Get customer balance
def get_balance(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM customers WHERE id = %s",
        (customer_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return float(result[0])

    return 0.0


# Create bank account
def create_account(name, email, opening_balance):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO customers (name, email, balance)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, opening_balance))

    conn.commit()
    conn.close()


# Deposit money
def deposit_money(customer_id, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE customers SET balance = balance + %s WHERE id = %s",
        (amount, customer_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("Customer not found")

    cursor.execute(
        """
        INSERT INTO transactions
        (customer_id, transaction_type, amount)
        VALUES (%s, 'DEPOSIT', %s)
        """,
        (customer_id, amount)
    )

    conn.commit()
    conn.close()


# Withdraw money
def withdraw_money(customer_id, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET balance = balance - %s
        WHERE id = %s AND balance >= %s
        """,
        (amount, customer_id, amount)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("Insufficient balance or invalid account")

    cursor.execute(
        """
        INSERT INTO transactions
        (customer_id, transaction_type, amount)
        VALUES (%s, 'WITHDRAW', %s)
        """,
        (customer_id, amount)
    )

    conn.commit()
    conn.close()


# Get transaction history
def get_transactions():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT t.id, c.name, t.transaction_type,
               t.amount, t.created_at
        FROM transactions t
        JOIN customers c ON t.customer_id = c.id
        ORDER BY t.created_at DESC
    """

    cursor.execute(query)

    transactions = cursor.fetchall()

    conn.close()

    return transactions