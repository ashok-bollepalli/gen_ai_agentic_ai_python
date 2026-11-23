import mysql.connector
import pandas as pd


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="loan_db"
    )
    return connection


def load_data():
    connection = get_connection()
    query = "select * from loan_applications"
    df = pd.read_sql(query, connection)
    connection.close()
    return df
