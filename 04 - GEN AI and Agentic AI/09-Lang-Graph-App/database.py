import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# MySQL Connection
engine = create_engine(
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@localhost/banking_ai"
)


# Execute Database Query
def execute_db_query(question):

    question = question.lower()

    if "transaction" in question:
        query = """
        SELECT * FROM transactions
        LIMIT 100
        """

    elif "savings" in question:
        query = """
        SELECT * FROM accounts
        WHERE account_type = 'SAVINGS'
        """

    elif "count" in question:
        query = """
        SELECT COUNT(*) AS total_accounts
        FROM accounts
        """

    elif "failed" in question:
        query = """
        SELECT * FROM transactions
        WHERE status = 'FAILED'
        """

    else:
        query = """
        SELECT * FROM accounts
        """

    # Execute SQL Query
    df = pd.read_sql(query, engine)

    # Return Result
    return df.to_string(index=False)