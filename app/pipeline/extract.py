import sqlite3
import pandas as pd


def extract_data(database_path):
    """
    Load raw production data from SQLite database.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT *
    FROM produktionsdaten
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df