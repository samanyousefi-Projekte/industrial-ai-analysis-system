import pandas as pd


def transform_data(df):
    """
    Clean and transform raw production data.
    """


    # Convert percentage columns from string to float
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


    # Convert energy columns from string to float
    # Example: "0,318" -> 0.318

    energy_columns = [
        "Energieverbrauch (kWh)",
        "Energie-pro-Stück (kWh)"
    ]

    for column in energy_columns:
        df[column] = (
            df[column]
            .str.replace(",", ".", regex=False)
            .astype(float)
        )


    # Convert date column to datetime format

    df["Datum"] = pd.to_datetime(df["Datum"])


    # Rename columns to an AI-friendly schema

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

        "Energieverbrauch (kWh)": 
            "energy_consumption_kwh",

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


    return df