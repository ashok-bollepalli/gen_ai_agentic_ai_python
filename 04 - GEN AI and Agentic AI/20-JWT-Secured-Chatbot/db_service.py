"""
db_service.py - MySQL access: create table, register user, login user.
"""
import bcrypt
import mysql.connector
from config import config

DB = dict(host=config.DB_HOST, port=config.DB_PORT,
          user=config.DB_USER, password=config.DB_PASSWORD)


def run(sql, params=(), fetch=False, database=config.DB_NAME):
    """Run one SQL query. Returns one row as a dict when fetch=True."""
    conn = mysql.connector.connect(**DB, database=database)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        if fetch:
            return cursor.fetchone()
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def init_db():
    run(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}", database=None)
    run("""
        CREATE TABLE IF NOT EXISTS users (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            username      VARCHAR(50)  NOT NULL UNIQUE,
            email         VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def register_user(username, email, password):
    """Returns False if username or email already exists."""
    try:
        run("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hash_password(password)))
        return True
    except mysql.connector.IntegrityError:
        return False


def login_user(username, password):
    """Returns the user row if the password matches, else None."""
    user = run("SELECT * FROM users WHERE username = %s", (username,), fetch=True)
    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return user
    return None