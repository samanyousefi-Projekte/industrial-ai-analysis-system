from app.analytics.production_analysis import (
    get_downtime_by_machine,
    get_scrap_by_machine,
    get_oee_by_machine,
    get_error_analysis_by_machine
)

from app.insights.report_generator import generate_report


def analyze_production_problem(database_path):
    """
    Combine multiple KPIs and generate root cause insights.
    """

    # ---------------------------------
    # Get KPI results
    # ---------------------------------

    downtime = get_downtime_by_machine(
        database_path
    )

    scrap = get_scrap_by_machine(
        database_path
    )

    oee = get_oee_by_machine(
        database_path
    )


    # ---------------------------------
    # Identify problematic machine
    # ---------------------------------

    worst_downtime_machine = (
        downtime.iloc[0]["machine_id"]
    )

    highest_scrap_machine = (
        scrap.iloc[0]["machine_id"]
    )

    lowest_oee_machine = (
        oee.iloc[0]["machine_id"]
    )


    # ---------------------------------
    # Combine evidence
    # ---------------------------------

    if (
        worst_downtime_machine
        == highest_scrap_machine
        == lowest_oee_machine
    ):

        problem_machine = (
            worst_downtime_machine
        )

    else:

        problem_machine = None


    # ---------------------------------
    # Analyze errors only for
    # the detected problem machine
    # ---------------------------------

    if problem_machine:

        errors = get_error_analysis_by_machine(
            database_path,
            problem_machine
        )

    else:

        errors = None


    # ---------------------------------
    # Generate insight report
    # ---------------------------------

    report = {

        "problem_machine": (
            problem_machine
            if problem_machine
            else "No clear problem detected"
        ),

        "highest_downtime": {
            "machine": worst_downtime_machine,
            "minutes": int(
                downtime.iloc[0][
                    "total_downtime"
                ]
            )
        },

        "highest_scrap": {
            "machine": highest_scrap_machine,
            "quantity": int(
                scrap.iloc[0][
                    "total_scrap"
                ]
            )
        },

        "lowest_oee": {
            "machine": lowest_oee_machine,
            "oee": float(
                round(
                    oee.iloc[0][
                        "average_oee"
                    ],
                    2
                )
            )
        },

        "main_errors": (
            errors.head(3).to_dict(
                orient="records"
            )
            if errors is not None
            else []
        )
    }


    return report


if __name__ == "__main__":

    database = (
        "database/production_clean.db"
    )

    result = analyze_production_problem(
        database
    )

    report = generate_report(
        result
    )

    print(report)