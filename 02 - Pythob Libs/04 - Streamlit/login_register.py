
import streamlit as st
import sqlite3
import hashlib
import secrets
import re

# -------------------------------
# 1. Page Configuration
# -------------------------------
st.set_page_config(
    page_title="User Authentication",
    page_icon="🔐",
    layout="centered"
)

# -------------------------------
# 2. Database Connection
# -------------------------------
def get_connection():
    return sqlite3.connect("users.db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# -------------------------------
# 3. Password Hashing
# -------------------------------
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        600000
    )

    return salt + "$" + hashed.hex()

def verify_password(password, stored_hash):
    try:
        salt, _ = stored_hash.split("$", 1)
        return secrets.compare_digest(
            hash_password(password, salt),
            stored_hash
        )
    except (ValueError, TypeError):
        return False

# -------------------------------
# 4. Register User
# -------------------------------
def register_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) "
            "VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()

# -------------------------------
# 5. Login User
# -------------------------------
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, password_hash "
        "FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user[3]):
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }

    return None

# -------------------------------
# 6. Custom UI Styling
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f0fdfa);
}
.auth-title {
    text-align: center;
    color: #3730a3;
    font-size: 32px;
    font-weight: 700;
}
.auth-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}
div.stButton > button {
    width: 100%;
    background-color: #4f46e5;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #3730a3;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Create database table when app starts
create_table()

# Session state initialization
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------
# 7. Navigation
# -------------------------------
st.sidebar.title("🔐 My Application")

if st.session_state.user:
    page = "Dashboard"
    st.sidebar.success(
        f"Logged in as {st.session_state.user['name']}"
    )
else:
    page = st.sidebar.radio(
        "Navigation",
        ["Login", "Register"]
    )

# -------------------------------
# 8. Registration Page
# -------------------------------
if page == "Register":
    st.markdown(
        '<div class="auth-title">Create Account</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="auth-subtitle">'
        'Join us today!</div>',
        unsafe_allow_html=True
    )

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input(
            "Password", type="password"
        )
        confirm_password = st.text_input(
            "Confirm Password", type="password"
        )

        submitted = st.form_submit_button(
            "Create Account"
        )

    if submitted:
        name = name.strip()
        email = email.strip().lower()

        if not name or not email or not password:
            st.error("Please fill in all required fields.")

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
        ):
            st.error("Please enter a valid email address.")

        elif len(password) < 8:
            st.error("Password must contain at least 8 characters.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            success = register_user(name, email, password)

            if success:
                st.success(
                    "Registration successful! "
                    "Select Login from the sidebar."
                )
            else:
                st.error("This email is already registered.")

# -------------------------------
# 9. Login Page
# -------------------------------
elif page == "Login":
    st.markdown(
        '<div class="auth-title">Welcome Back!</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="auth-subtitle">'
        'Login to access your account</div>',
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input(
            "Password", type="password"
        )

        submitted = st.form_submit_button("Login")

    if submitted:
        email = email.strip().lower()

        user = login_user(email, password)

        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid email or password.")

# -------------------------------
# 10. Dashboard Page
# -------------------------------
elif page == "Dashboard":
    user = st.session_state.user

    st.title(f"Welcome, {user['name']}! 👋")
    st.success("You have logged in successfully.")

    st.subheader("Your Profile")
    st.write("**User ID:**", user["id"])
    st.write("**Name:**", user["name"])
    st.write("**Email:**", user["email"])

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
