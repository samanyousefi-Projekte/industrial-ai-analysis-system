def validate_data(df):
    """
    Validate cleaned production data quality.
    Returns True if all checks pass.
    """


    # Check required columns

    required_columns = [
        "machine_id",
        "production_quantity",
        "downtime_minutes",
        "oee_percent",
        "availability_percent"
    ]


    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )


    # Check missing values

    missing_values = df[required_columns].isnull().sum()


    if missing_values.any():
        raise ValueError(
            f"Missing values found:\n{missing_values}"
        )


    # Check KPI ranges

    if not df["oee_percent"].between(0, 100).all():
        raise ValueError(
            "OEE values outside valid range."
        )


    if not df["availability_percent"].between(0, 100).all():
        raise ValueError(
            "Availability values outside valid range."
        )


    # Check negative values

    numeric_columns = [
        "production_quantity",
        "scrap_quantity",
        "downtime_minutes",
        "energy_consumption_kwh"
    ]


    for column in numeric_columns:
        if (df[column] < 0).any():
            raise ValueError(
                f"Negative values found in {column}"
            )


    print("Data validation passed successfully.")

    return True