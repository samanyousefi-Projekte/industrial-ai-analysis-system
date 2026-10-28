import sqlite3
import pandas as pd


# Path to the original database
input_database = "database/production_analysis.db"

# Path for the cleaned database output
output_database = "database/production_clean.db"


# Connect to the original SQLite database
connection = sqlite3.connect(input_database)


# Load production data from the original table
query = """
SELECT *
FROM produktionsdaten
"""

df = pd.read_sql_query(query, connection)

connection.close()


print("Original data loaded:")
print(df.shape)


#################
# Data Cleaning #
#################

# Convert percentage columns from string format to numeric values
# Example: "94,9%" -> 94.9

percent_columns = [
    "Ausschussquote (%)",
    "Verfügbarkeit (%)",
    "OEE-einfach (%)"
]


for column in percent_columns:
    df[column] = (
        df[column]
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )


# Convert energy-related columns from string format to numeric values
# Example: "393,5" -> 393.5

numeric_columns = [
    "Energieverbrauch (kWh)",
    "Energie-pro-Stück (kWh)"
]


for column in numeric_columns:
    df[column] = (
        df[column]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )


# Convert date column from string format to datetime format

df["Datum"] = pd.to_datetime(df["Datum"])


##################
# Rename Columns #
##################

# Rename columns to follow a consistent English naming convention
# This improves readability for SQL queries, APIs and AI agents.

column_mapping = {

    "Datum": "date",
    "Maschine": "machine_id",
    "Auftrag": "order_id",
    "Produkt": "product",
    "Schicht": "shift",

    "Produktionsmenge": "production_quantity",
    "Ausschuss": "scrap_quantity",

    "Stillstandszeit (min)": "downtime_minutes",

    "Fehlerart": "error_type",

    "Energieverbrauch (kWh)": "energy_consumption_kwh",

    "Status": "status",

    "Geplante-Produktionszeit (min)": 
        "planned_production_time_minutes",

    "Gutmenge": "good_quantity",

    "Ausschussquote (%)":
        "scrap_rate_percent",

    "Verfügbarkeit (%)":
        "availability_percent",

    "Energie-pro-Stück (kWh)":
        "energy_per_piece_kwh",

    "OEE-einfach (%)":
        "oee_percent"
}


df.rename(
    columns=column_mapping,
    inplace=True
)


print("\nCleaned columns:")
print(df.columns.tolist())


#######################
# Save Clean Database #  
#######################

# Store the cleaned dataset in a new SQLite database.
# The original database remains unchanged.

connection = sqlite3.connect(output_database)


df.to_sql(
    "production_data",
    connection,
    if_exists="replace",
    index=False
)


connection.close()


print("\nClean database created:")
print(output_database)