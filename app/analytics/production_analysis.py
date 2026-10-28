import sqlite3
import pandas as pd


def get_downtime_by_machine(database_path):
    """
    Calculate total downtime per machine.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        machine_id,
        SUM(downtime_minutes) AS total_downtime
    FROM production_data
    GROUP BY machine_id
    ORDER BY total_downtime DESC;
    """

    result = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return result


def get_scrap_by_machine(database_path):
    """
    Calculate total scrap quantity per machine.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        machine_id,
        SUM(scrap_quantity) AS total_scrap
    FROM production_data
    GROUP BY machine_id
    ORDER BY total_scrap DESC;
    """

    result = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return result


def get_oee_by_machine(database_path):
    """
    Calculate average OEE percentage per machine.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        machine_id,
        AVG(oee_percent) AS average_oee
    FROM production_data
    GROUP BY machine_id
    ORDER BY average_oee ASC;
    """

    result = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return result


def get_error_analysis(database_path):
    """
    Analyze frequency of error types across all machines.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        error_type,
        COUNT(*) AS error_count
    FROM production_data
    WHERE error_type != 'Kein Fehler'
    GROUP BY error_type
    ORDER BY error_count DESC;
    """

    result = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return result


def get_error_analysis_by_machine(
    database_path,
    machine_id
):
    """
    Analyze frequency of error types
    for one specific machine.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        error_type,
        COUNT(*) AS error_count
    FROM production_data
    WHERE machine_id = ?
      AND error_type != 'Kein Fehler'
    GROUP BY error_type
    ORDER BY error_count DESC;
    """

    result = pd.read_sql_query(
        query,
        connection,
        params=(machine_id,)
    )

    connection.close()

    return result


def get_machine_performance(
    database_path,
    machine_id
):
    """
    Get performance KPIs for one specific machine.
    """

    connection = sqlite3.connect(database_path)

    query = """
    SELECT
        machine_id,
        AVG(oee_percent) AS average_oee,
        SUM(downtime_minutes) AS total_downtime,
        SUM(scrap_quantity) AS total_scrap,
        SUM(production_quantity) AS total_production,
        SUM(good_quantity) AS total_good_quantity
    FROM production_data
    WHERE machine_id = ?
    GROUP BY machine_id;
    """

    result = pd.read_sql_query(
        query,
        connection,
        params=(machine_id,)
    )

    connection.close()

    return result


if __name__ == "__main__":

    database = "database/production_clean.db"

    print("Downtime analysis:")
    downtime_analysis = get_downtime_by_machine(
        database
    )
    print(downtime_analysis)

    print("\nScrap analysis:")
    scrap_analysis = get_scrap_by_machine(
        database
    )
    print(scrap_analysis)

    print("\nOEE analysis:")
    oee_analysis = get_oee_by_machine(
        database
    )
    print(oee_analysis)

    print("\nError analysis:")
    error_analysis = get_error_analysis(
        database
    )
    print(error_analysis)

    print("\nM2 error analysis:")
    m2_error_analysis = get_error_analysis_by_machine(
        database,
        "M2"
    )
    print(m2_error_analysis)