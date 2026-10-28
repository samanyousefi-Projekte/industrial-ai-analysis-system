from langchain_core.tools import tool

from app.agent.response_formatter import format_response

from app.analytics.production_analysis import (
    get_downtime_by_machine,
    get_scrap_by_machine,
    get_oee_by_machine,
    get_error_analysis,
    get_machine_performance
)

from app.insights.root_cause_analysis import (
    analyze_production_problem
)


DATABASE = "database/production_clean.db"



# ---------------------------------
# Downtime Analysis Tool
# ---------------------------------

@tool
def downtime_analysis():
    """
    Find machines with highest downtime.
    Use this tool when the user asks about:
    - production interruptions
    - machine stops
    - downtime
    """

    result = get_downtime_by_machine(DATABASE)

    return format_response(
        result,
        "downtime"
    )



# ---------------------------------
# Scrap Analysis Tool
# ---------------------------------

@tool
def scrap_analysis():
    """
    Find machines with highest scrap quantity.
    Use this tool when the user asks about:
    - scrap
    - rejected products
    - waste quantity
    """

    result = get_scrap_by_machine(DATABASE)

    return format_response(
        result,
        "scrap"
    )



# ---------------------------------
# OEE Analysis Tool
# ---------------------------------

@tool
def oee_analysis():
    """
    Compare OEE values across machines.

    Use this tool when the user asks about:
    - OEE ranking
    - lowest OEE
    - highest OEE
    - efficiency comparison between machines
    """

    result = get_oee_by_machine(DATABASE)

    return format_response(
        result,
        "oee"
    )



# ---------------------------------
# Error Analysis Tool
# ---------------------------------

@tool
def error_analysis():
    """
    Find the most common production errors.
    Use this tool when the user asks about:
    - failure types
    - common errors
    - error frequency
    """

    result = get_error_analysis(DATABASE)

    return format_response(
        result,
        "errors"
    )

#---------------------------------
# Machine Performance Tool  
#---------------------------------

@tool
def machine_performance(machine_id: str):
    """
    Analyze the overall performance of one specific machine.

    Use this tool when the user asks:
    - How is machine M1 performing?
    - What is the performance of M3?
    - Show KPIs for M2.
    - Give me the performance data for a specific machine.

    Returns:
    - OEE
    - downtime
    - scrap
    - total production
    - good quantity
    """

    result = get_machine_performance(
        DATABASE,
        machine_id.upper()
    )

    return format_response(
        result,
        "machine_performance"
    )


# ---------------------------------
# Root Cause Analysis Tool
# ---------------------------------

@tool
def root_cause_analysis():
    """
    Investigate why a machine is performing badly.

    Use this tool when the user asks:
    - Why is this machine bad?
    - What is the root cause?
    - What is the main production problem?
    - What should we investigate first?

    This tool combines:
    - downtime analysis
    - scrap analysis
    - OEE analysis
    - error analysis

    Use this instead of error_analysis
    for "why" or "reason" questions.
    """


    result = analyze_production_problem(DATABASE)


    return format_response(
        result,
        "root_cause"
    )



# ---------------------------------
# Available Agent Tools
# ---------------------------------

tools = [

    downtime_analysis,

    scrap_analysis,

    oee_analysis,

    error_analysis,

    root_cause_analysis,

    machine_performance

]