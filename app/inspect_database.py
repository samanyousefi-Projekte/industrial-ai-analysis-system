import sqlite3


database_path = "database/production_analysis.db"


connection = sqlite3.connect(database_path)

cursor = connection.cursor()


table_name = "produktionsdaten"


cursor.execute(f"PRAGMA table_info({table_name});")

columns = cursor.fetchall()


print(f"Schema of table: {table_name}")
print("-" * 50)


for column in columns:
    column_id = column[0]
    column_name = column[1]
    data_type = column[2]

    print(f"{column_id}: {column_name} ({data_type})")


connection.close()