import sys
import os
import re
import sqlite3


# ---------------------------------
# Add project root to Python path
# ---------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


import altair as alt
import streamlit as st

from app.agent.llm_agent import (
    agent,
    build_safe_final_answer
)

from app.analytics.production_analysis import (
    get_oee_by_machine,
    get_downtime_by_machine,
    get_scrap_by_machine,
    get_error_analysis
)


DATABASE = "database/production_clean.db"


# ---------------------------------
# Machine chart configuration
# ---------------------------------

MACHINE_IDS = [
    "M1",
    "M2",
    "M3",
    "M4"
]

MACHINE_COLORS = [
    "blue",
    "yellow",
    "red",
    "green"
]


# ---------------------------------
# Detect machine ID
# ---------------------------------

def detect_machine_id(text):
    """
    Detect machine IDs such as M1, M2, M3 or M4
    from user questions or AI answers.
    """

    if not text:
        return None

    match = re.search(
        r"\bM[1-4]\b",
        text.upper()
    )

    if match:
        return match.group(0)

    return None


# ---------------------------------
# Load KPI values for one machine
# ---------------------------------

def get_machine_kpis(machine_id):
    """
    Load average OEE, total downtime and total scrap
    for a selected machine from SQLite.
    """

    connection = sqlite3.connect(DATABASE)

    query = """
    SELECT
        machine_id,
        AVG(oee_percent) AS average_oee,
        SUM(downtime_minutes) AS total_downtime,
        SUM(scrap_quantity) AS total_scrap
    FROM production_data
    WHERE machine_id = ?
    GROUP BY machine_id;
    """

    cursor = connection.cursor()

    cursor.execute(
        query,
        (machine_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return {
        "machine_id": result[0],
        "oee": round(float(result[1]), 2),
        "downtime": int(result[2]),
        "scrap": int(result[3])
    }


# ---------------------------------
# Page configuration
# ---------------------------------

st.set_page_config(
    page_title="Industrial AI Assistant",
    page_icon="🏭",
    layout="centered"
)


# ---------------------------------
# Custom metric color
# ---------------------------------

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        color: #A855F7;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------
# Header
# ---------------------------------

st.title("🏭 Industrial AI Assistant")

st.write(
    "Ask questions about production performance, "
    "OEE, downtime, errors, and root causes."
)


# ---------------------------------
# Global Production KPI Cards
# ---------------------------------

oee_data_global = get_oee_by_machine(DATABASE)
downtime_data_global = get_downtime_by_machine(DATABASE)
scrap_data_global = get_scrap_by_machine(DATABASE)


overall_oee = round(
    float(
        oee_data_global["average_oee"].mean()
    ),
    2
)


total_downtime = int(
    downtime_data_global[
        "total_downtime"
    ].sum()
)


total_scrap = int(
    scrap_data_global[
        "total_scrap"
    ].sum()
)


kpi_col1, kpi_col2, kpi_col3 = st.columns(3)


with kpi_col1:

    st.metric(
        label="Overall OEE",
        value=f"{overall_oee} %"
    )


with kpi_col2:

    st.metric(
        label="Total Downtime",
        value=f"{total_downtime:,} min"
    )


with kpi_col3:

    st.metric(
        label="Total Scrap",
        value=f"{total_scrap:,} pcs"
    )


# ---------------------------------
# Dashboard Overview
# ---------------------------------

col1, col2 = st.columns(2)


# ---------------------------------
# OEE Chart
# ---------------------------------

with col1:

    st.subheader("OEE Overview")

    oee_data = get_oee_by_machine(
        DATABASE
    )

    oee_chart = alt.Chart(
        oee_data
    ).mark_bar().encode(

        x=alt.X(
            "machine_id:N",
            title="Machine"
        ),

        y=alt.Y(
            "average_oee:Q",
            title="OEE (%)"
        ),

        color=alt.Color(
            "machine_id:N",
            scale=alt.Scale(
                domain=MACHINE_IDS,
                range=MACHINE_COLORS
            ),
            legend=None
        ),

        tooltip=[
            "machine_id",
            "average_oee"
        ]

    ).properties(
        height=300
    )

    st.altair_chart(
        oee_chart,
        use_container_width=True
    )


# ---------------------------------
# Downtime Chart
# ---------------------------------

with col2:

    st.subheader("Downtime Overview")

    downtime_data = get_downtime_by_machine(
        DATABASE
    )

    downtime_chart = alt.Chart(
        downtime_data
    ).mark_bar().encode(

        x=alt.X(
            "machine_id:N",
            title="Machine"
        ),

        y=alt.Y(
            "total_downtime:Q",
            title="Downtime (min)"
        ),

        color=alt.Color(
            "machine_id:N",
            scale=alt.Scale(
                domain=MACHINE_IDS,
                range=MACHINE_COLORS
            ),
            legend=None
        ),

        tooltip=[
            "machine_id",
            "total_downtime"
        ]

    ).properties(
        height=300
    )

    st.altair_chart(
        downtime_chart,
        use_container_width=True
    )


# ---------------------------------
# Scrap Chart
# ---------------------------------

st.subheader("Scrap Overview")

scrap_data = get_scrap_by_machine(
    DATABASE
)

scrap_chart = alt.Chart(
    scrap_data
).mark_bar().encode(

    x=alt.X(
        "machine_id:N",
        title="Machine"
    ),

    y=alt.Y(
        "total_scrap:Q",
        title="Scrap (units)"
    ),

    color=alt.Color(
        "machine_id:N",
        scale=alt.Scale(
            domain=MACHINE_IDS,
            range=MACHINE_COLORS
        ),
        legend=None
    ),

    tooltip=[
        "machine_id",
        "total_scrap"
    ]

).properties(
    height=300
)

st.altair_chart(
    scrap_chart,
    use_container_width=True
)


# ---------------------------------
# Error Overview
# ---------------------------------

st.subheader("Error Overview")

error_data = get_error_analysis(
    DATABASE
)

error_chart = alt.Chart(
    error_data
).mark_bar().encode(

    x=alt.X(
        "error_count:Q",
        title="Occurrences"
    ),

    y=alt.Y(
        "error_type:N",
        title="Error Type",
        sort="-x"
    ),

    tooltip=[
        "error_type",
        "error_count"
    ]

).properties(
    height=300
)

st.altair_chart(
    error_chart,
    use_container_width=True
)


# ---------------------------------
# Initialize chat history
# ---------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------
# Clear Chat Button
# ---------------------------------

if st.button("Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# ---------------------------------
# Display previous messages
# ---------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------
# User question
# ---------------------------------

question = st.chat_input(
    "Ask a production question..."
)


# ---------------------------------
# Process question
# ---------------------------------

if question:

    # Save user question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Display user question
    with st.chat_message("user"):

        st.markdown(question)


    # Run AI Agent
    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing production data..."
        ):

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }
            )

            # Use Response Guard
            answer = build_safe_final_answer(
                response
            )


        # ---------------------------------
        # Detect machine dynamically
        # ---------------------------------

        machine_id = detect_machine_id(
            question
        )


        # If the user did not name a machine,
        # detect one only for comparison questions.
        if not machine_id:

            comparison_keywords = [
                "lowest",
                "highest",
                "best",
                "worst",
                "which machine",
                "compare"
            ]

            question_lower = (
                question.lower()
                if question
                else ""
            )

            is_comparison_question = any(
                keyword in question_lower
                for keyword in comparison_keywords
            )

            if is_comparison_question:

                machine_id = detect_machine_id(
                    answer
                )


        # ---------------------------------
        # Dynamic KPI Cards
        # ---------------------------------

        if machine_id:

            kpis = get_machine_kpis(
                machine_id
            )

            if kpis:

                st.caption(
                    f"Machine {machine_id} — KPI Summary"
                )

                (
                    machine_kpi_col1,
                    machine_kpi_col2,
                    machine_kpi_col3
                ) = st.columns(3)


                with machine_kpi_col1:

                    st.metric(
                        label="OEE",
                        value=f"{kpis['oee']} %"
                    )


                with machine_kpi_col2:

                    st.metric(
                        label="Downtime",
                        value=f"{kpis['downtime']} min"
                    )


                with machine_kpi_col3:

                    st.metric(
                        label="Scrap",
                        value=f"{kpis['scrap']} pcs"
                    )


        # ---------------------------------
        # Display AI answer
        # ---------------------------------

        st.markdown(answer)


    # ---------------------------------
    # Save assistant answer
    # ---------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )