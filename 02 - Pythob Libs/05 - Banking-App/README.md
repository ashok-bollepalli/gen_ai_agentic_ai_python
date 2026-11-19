# Simple Banking Management System

A beginner-friendly mini project using Python, MySQL, NumPy, Pandas, Matplotlib and Streamlit.

## Features
- Create a customer bank account
- Deposit money
- Withdraw money with balance validation
- View customer balances
- View transaction history
- Dashboard with total balance, average balance and a chart

## Setup

1. Install Python and MySQL.
2. Create the database and tables by running `schema.sql` in MySQL Workbench:

   ```sql
   SOURCE /full/path/to/schema.sql;
   ```

   Alternatively, execute the SQL statements in `schema.sql` manually.

3. Open `db.py` and update `user` and `password` in `DB_CONFIG`.
4. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application from this folder:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown by Streamlit, usually http://localhost:8501.

## Where each library is used
- **MySQL:** stores customer accounts and transactions.
- **NumPy:** calculates the average account balance.
- **Pandas:** converts database records into DataFrames and groups transactions.
- **Matplotlib:** displays customer account balances as a bar chart.
- **Streamlit:** provides the web user interface.

## Learning note
This is a classroom/demo project, not production banking software. A real banking system needs authentication, authorization, audit logs, database transactions/locking, input validation, encryption, and stronger security controls.
