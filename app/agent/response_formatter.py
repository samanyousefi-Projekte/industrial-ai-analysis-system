def format_response(result, intent):
    """
    Convert analysis results into human-readable industrial reports.
    """


    # -------------------------
    # Downtime
    # -------------------------

    if intent == "downtime":

        response = """
Downtime Analysis Report

Machine Ranking:

"""

        ranking = result.sort_values(
            by="total_downtime",
            ascending=False
        )

        for _, row in ranking.iterrows():

            response += (
                f"- {row['machine_id']}: "
                f"{int(row['total_downtime'])} minutes\n"
            )

        top_machine = ranking.iloc[0]

        response += f"""

Highest Downtime Machine:

{top_machine['machine_id']}

Total Downtime:
{int(top_machine['total_downtime'])} minutes

"""

        return response


    # -------------------------
    # Scrap
    # -------------------------

    elif intent == "scrap":

        response = """
Scrap Analysis Report

Machine Ranking:

"""

        ranking = result.sort_values(
            by="total_scrap",
            ascending=False
        )

        for _, row in ranking.iterrows():

            response += (
                f"- {row['machine_id']}: "
                f"{int(row['total_scrap'])} pieces\n"
            )

        top_machine = ranking.iloc[0]

        response += f"""

Highest Scrap Machine:

{top_machine['machine_id']}

Total Scrap:
{int(top_machine['total_scrap'])} pieces

"""

        return response


    # -------------------------
    # OEE
    # -------------------------

    elif intent == "oee":

        response = """
OEE Performance Report

Machine Ranking:

"""

        ranking = result.sort_values(
            by="average_oee",
            ascending=False
        )

        for _, row in ranking.iterrows():

            response += (
                f"- {row['machine_id']}: "
                f"{round(float(row['average_oee']), 2)} %\n"
            )

        lowest = result.sort_values(
            by="average_oee",
            ascending=True
        ).iloc[0]

        response += f"""

Lowest OEE Machine:

{lowest['machine_id']}

OEE:
{round(float(lowest['average_oee']), 2)} %

"""

        return response


    # -------------------------
    # Errors
    # -------------------------

    elif intent == "errors":

        response = """
Production Error Analysis

Most Common Errors:

"""

        for _, row in result.head(5).iterrows():

            response += (
                f"- {row['error_type']}: "
                f"{row['error_count']} occurrences\n"
            )

        return response


    # -------------------------
    # Root Cause Investigation
    # -------------------------

    elif intent == "root_cause":

        response = f"""
Production Problem Investigation Report

Problem Machine:

{result['problem_machine']}

Performance Evidence:

- Highest Downtime:
  {result['highest_downtime']['minutes']} minutes

- Highest Scrap:
  {result['highest_scrap']['quantity']} pieces

- Lowest OEE:
  {result['lowest_oee']['oee']} %

Most Frequent Errors on {result['problem_machine']}:

"""

        for error in result["main_errors"]:

            response += (
                f"- {error['error_type']}: "
                f"{error['error_count']} occurrences\n"
            )

        response += """

Interpretation:

These error frequencies identify areas that should be investigated.
The available data does not prove that these errors directly caused
the measured downtime, scrap, or OEE values.

Recommended Investigation:

- Review the most frequent recorded errors.
- Inspect relevant sensors and machine components where applicable.
- Review maintenance records and maintenance events.
- Check material-related incidents where applicable.
- Compare error timestamps with downtime and production events
  before confirming a causal relationship.

"""

        return response


    # -------------------------
    # Machine Performance
    # -------------------------

    elif intent == "machine_performance":

        if result.empty:
            return "No performance data available for this machine."

        machine = result.iloc[0]

        return f"""
Machine Performance Report

Machine:
{machine['machine_id']}

KPIs:

- OEE:
  {round(float(machine['average_oee']), 2)} %

- Downtime:
  {int(machine['total_downtime'])} minutes

- Scrap:
  {int(machine['total_scrap'])} pieces

- Total Production:
  {int(machine['total_production'])} pieces

- Good Quantity:
  {int(machine['total_good_quantity'])} pieces
"""


    else:

        return "No response available."