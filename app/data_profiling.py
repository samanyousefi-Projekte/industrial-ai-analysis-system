import sqlite3
import pandas as pd


database_path = "database/production_analysis.db"


connection = sqlite3.connect(database_path)


query = """
SELECT *
FROM produktionsdaten
"""


df = pd.read_sql_query(query, connection)


connection.close()


print("Number of rows:")
print(len(df))


print("\nColumns:")
print(df.columns.tolist())


print("\nMissing values:")
print(df.isnull().sum())


print("\nData types:")
print(df.dtypes)


print("\nFirst 5 rows:")
print(df.head())