
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from db import setup_database
from backend import (
    get_customers, get_balance, create_account,
    deposit_money, withdraw_money, get_transactions
)

# Page Configuration
st.set_page_config(page_title="Banking System", page_icon="🏦", layout="wide")
setup_database()

# Success Message
if "message" in st.session_state and st.session_state.message:
    st.success(st.session_state.message)
    st.session_state.message = None

# Application Header
st.title("🏦 Simple Banking Management System")
st.caption("Python | MySQL | NumPy | Pandas | Matplotlib | Streamlit")

# Sidebar Menu
menu = st.sidebar.radio("Choose an Option", [
    "Dashboard", "Create Account", "Deposit", "Withdraw", "Transactions"
])

# Load Customers
try:
    with st.spinner("Loading customers..."):
        customers = get_customers()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.subheader("📊 Bank Dashboard")

    total_customers = len(customers)
    total_balance = sum(float(c["balance"]) for c in customers)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", total_customers)
    col2.metric("Total Balance", f"₹{total_balance:,.2f}")

    average = total_balance / total_customers if total_customers else 0
    col3.metric("Average Balance", f"₹{average:,.2f}")

    if customers:
        df = pd.DataFrame(customers)

        st.subheader("Customer Accounts")
        st.dataframe(df[["id", "name", "email", "balance"]], use_container_width=True)

        # NumPy
        balances = np.array(df["balance"], dtype=float)
        st.metric("Average Balance (NumPy)", f"₹{np.mean(balances):,.2f}")

        # Matplotlib
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar(df["name"], balances)
        ax.set_title("Customer Account Balances")
        ax.set_xlabel("Customer")
        ax.set_ylabel("Balance (₹)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No accounts found. Please create an account.")


# ---------------- CREATE ACCOUNT ----------------

elif menu == "Create Account":

    st.subheader("➕ Create New Bank Account")

    with st.form("create_account"):
        name = st.text_input("Customer Name")
        email = st.text_input("Email Address")
        opening_balance = st.number_input("Opening Balance (₹)", min_value=0.0, step=500.0)
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if not name.strip() or not email.strip():
            st.error("Please enter all required details.")
        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email address.")
        else:
            try:
                with st.spinner("Creating account..."):
                    create_account(name.strip(), email.strip(), opening_balance)

                st.session_state.message = "Account created successfully! 🎉"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


# ---------------- DEPOSIT / WITHDRAW ----------------

elif menu in ["Deposit", "Withdraw"]:

    st.subheader(f"💰 {menu} Money")

    if not customers:
        st.warning("Please create a customer account first.")
    else:
        options = {
            f'{c["name"]} (Account #{c["id"]})': c["id"]
            for c in customers
        }

        selected = st.selectbox("Select Customer", list(options.keys()))
        customer_id = options[selected]

        balance = get_balance(customer_id)
        st.info(f"Current Balance: ₹{balance:,.2f}")

        amount = st.number_input("Enter Amount (₹)", min_value=1.0, step=100.0)

        if st.button(menu, use_container_width=True):
            try:
                with st.spinner(f"Processing {menu.lower()}..."):
                    if menu == "Deposit":
                        deposit_money(customer_id, amount)
                    else:
                        withdraw_money(customer_id, amount)

                st.session_state.message = f"{menu} successful! ₹{amount:,.2f} 🎉"
                st.rerun()
            except Exception as e:
                st.error(f"Transaction failed: {e}")


# ---------------- TRANSACTIONS ----------------

elif menu == "Transactions":

    st.subheader("📋 Transaction History")

    try:
        with st.spinner("Loading transactions..."):
            rows = get_transactions()

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)

            summary = df.groupby("transaction_type")["amount"].sum()

            st.subheader("Deposit / Withdrawal Summary")
            st.bar_chart(summary)

        else:
            st.info("No transactions found.")

    except Exception as e:
        st.error(f"Error loading transactions: {e}")


# Footer
st.divider()
st.caption("🏦 Banking Management System | Python + MySQL + Streamlit")