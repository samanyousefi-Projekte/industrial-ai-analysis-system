def generate_report(analysis_result):
    """
    Generate human-readable production analysis report.
    """


    machine = analysis_result["problem_machine"]


    downtime = analysis_result["highest_downtime"]

    scrap = analysis_result["highest_scrap"]

    oee = analysis_result["lowest_oee"]

    errors = analysis_result["main_errors"]


    report = f"""
Production Analysis Report
==========================


Main Problem Machine:
{machine}


Evidence:

1. Highest downtime:
{downtime['minutes']} minutes


2. Highest scrap:
{scrap['quantity']} pieces


3. Lowest OEE:
{oee['oee']} %


Main Error Causes:

"""


    for error in errors:
        report += (
            f"- {error['error_type']}: "
            f"{error['error_count']} occurrences\n"
        )


    report += """

Recommendation:

Investigate the main error causes
and improve machine performance.
"""


    return report