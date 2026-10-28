from pipeline.extract import extract_data
from pipeline.transform import transform_data
from pipeline.validate import validate_data
from pipeline.load import load_data


# Input and output database paths

input_database = "database/production_analysis.db"

output_database = "database/production_clean.db"


def run_pipeline():
    """
    Execute complete ETL pipeline:
    Extract → Transform → Validate → Load
    """


    print("Starting data pipeline...")


    # Step 1: Extract raw data

    df = extract_data(input_database)

    print("Extract step completed.")
    print(f"Rows loaded: {len(df)}")


    # Step 2: Transform data

    df_clean = transform_data(df)

    print("Transform step completed.")


    # Step 3: Validate cleaned data

    validate_data(df_clean)

    print("Validation step completed.")


    # Step 4: Load data into clean database

    load_data(
        df_clean,
        output_database
    )


    print("Pipeline finished successfully.")


if __name__ == "__main__":
    run_pipeline()