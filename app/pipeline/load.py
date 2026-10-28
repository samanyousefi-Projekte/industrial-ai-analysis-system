import sqlite3


def load_data(df, database_path):
    """
    Save cleaned production data into SQLite database.
    """


    connection = sqlite3.connect(database_path)


    df.to_sql(
        "production_data",
        connection,
        if_exists="replace",
        index=False
    )


    connection.close()


    print("Clean data saved successfully.")