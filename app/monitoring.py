import json

from app.analytics.production_analysis import (
    get_oee_by_machine,
    get_downtime_by_machine,
    get_scrap_by_machine,
    get_error_analysis_by_machine
)


DATABASE = "database/production_clean.db"


# ---------------------------------
# Prototype monitoring thresholds
# ---------------------------------

OEE_CRITICAL_THRESHOLD = 80.0
DOWNTIME_CRITICAL_THRESHOLD = 6000
SCRAP_CRITICAL_THRESHOLD = 6000


def analyze_monitoring_status(database_path):
    """
    Analyze production KPIs and detect machines
    that require critical investigation.

    The thresholds are prototype values and can
    later be replaced by real production targets.
    """

    oee_data = get_oee_by_machine(
        database_path
    )

    downtime_data = get_downtime_by_machine(
        database_path
    )

    scrap_data = get_scrap_by_machine(
        database_path
    )


    # ---------------------------------
    # Combine KPI data
    # ---------------------------------

    monitoring_data = (
        oee_data
        .merge(
            downtime_data,
            on="machine_id"
        )
        .merge(
            scrap_data,
            on="machine_id"
        )
    )


    critical_machines = []


    # ---------------------------------
    # Evaluate each machine
    # ---------------------------------

    for _, row in monitoring_data.iterrows():

        machine_id = row["machine_id"]

        oee = round(
            float(row["average_oee"]),
            2
        )

        downtime = int(
            row["total_downtime"]
        )

        scrap = int(
            row["total_scrap"]
        )


        triggered_conditions = []


        # ---------------------------------
        # Critical conditions
        # ---------------------------------

        if oee < OEE_CRITICAL_THRESHOLD:

            triggered_conditions.append(
                "OEE below critical threshold"
            )


        if downtime > DOWNTIME_CRITICAL_THRESHOLD:

            triggered_conditions.append(
                "Downtime above critical threshold"
            )


        if scrap > SCRAP_CRITICAL_THRESHOLD:

            triggered_conditions.append(
                "Scrap above critical threshold"
            )


        # ---------------------------------
        # Critical classification
        # ---------------------------------

        # A machine is classified as critical
        # when at least two monitoring conditions
        # are triggered.

        if len(triggered_conditions) >= 2:

            errors = get_error_analysis_by_machine(
                database_path,
                machine_id
            )


            top_errors = (
                errors.head(3).to_dict(
                    orient="records"
                )
            )


            critical_machines.append(
                {
                    "machine": machine_id,

                    "status": "CRITICAL",

                    "oee": oee,

                    "downtime": downtime,

                    "scrap": scrap,

                    "triggered_conditions":
                        triggered_conditions,

                    "top_errors":
                        top_errors
                }
            )


    # ---------------------------------
    # Overall monitoring status
    # ---------------------------------

    if critical_machines:

        return {
            "status": "CRITICAL",

            "critical_machine_count":
                len(critical_machines),

            "critical_machines":
                critical_machines
        }


    return {
        "status": "NORMAL",

        "critical_machine_count": 0,

        "critical_machines": []
    }


# ---------------------------------
# Run monitoring
# ---------------------------------

if __name__ == "__main__":

    result = analyze_monitoring_status(
        DATABASE
    )


    # ---------------------------------
    # Save monitoring result as JSON
    # ---------------------------------

    output_file = (
        "data/monitoring_output.json"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )


    # ---------------------------------
    # Print monitoring result
    # ---------------------------------

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )


    print(
        f"\nMonitoring result saved to: "
        f"{output_file}"
    )