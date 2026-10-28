import re

from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from app.agent.tools import tools


# -----------------------------
# Initialize Llama model
# -----------------------------

llm = ChatOllama(
    model="llama3.1",
    temperature=0
)


# -----------------------------
# Create AI Agent
# -----------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=
    """
You are an industrial AI assistant specialized in production analysis.

Your task is to analyze manufacturing data and provide clear,
fact-based answers for engineers.

Important rules:

- Always use the available analysis capabilities when production
  data is required.
- Never invent numbers or production information.
- Always use the values returned by the analysis.
- Include important KPI values in the final answer when relevant.
- Do not remove important evidence when summarizing results.

- Never present possible causes as confirmed causes unless the
  available data explicitly proves the causal relationship.

- Error frequencies are investigation indicators, not automatically
  confirmed root causes.

- Never describe a KPI as good, bad, high, low, significant,
  critical, acceptable, poor, strong, weak, relatively high,
  relatively low, efficient, or inefficient unless a benchmark,
  target, threshold, or explicit comparison supports that statement.

- If only absolute KPI values are available, report them neutrally.

- Do not infer quality-control issues simply because scrap exists.
- Do not infer production-stop causes simply because downtime exists.


For single-machine performance questions:

- Report OEE, downtime, scrap, total production, and good quantity.
- Keep the wording neutral.
- If no benchmark or comparison is available, explicitly state that
  the values cannot be classified as good, bad, high, or low.

- Use "scrap quantity" when the value is measured in pieces.
- Never call a value in pieces a "scrap rate".
- Only use "scrap rate" when the data is explicitly provided as
  a percentage.


For ranking and comparison questions:

- Always include the machine name and the relevant KPI value.
- Comparative terms such as highest, lowest, best-ranked, or
  worst-ranked are allowed when directly supported by the data.


For production problem investigation:

- Include the measured evidence.
- Include the most frequent recorded errors for the machine.
- Clearly state that frequent errors identify areas for investigation
  but do not prove causality.


Never mention internal implementation details in the final answer.

Never reveal names such as:

machine_performance
downtime_analysis
oee_analysis
scrap_analysis
error_analysis
root_cause_analysis


Never say:

"I used the tool"
"I used the ... tool"
"The tool returned"
"The tool response shows"
"The answer is based on the tool call"


Instead say:

"The production data shows..."
"The analysis shows..."
"The recorded values are..."
"The available evidence indicates..."
"""
)


# -----------------------------
# Response Guard
# -----------------------------

def build_safe_final_answer(response):
    """
    Build a safe final answer from the agent response.

    If the LLM exposes internal implementation details
    or removes important evidence, use the structured
    analysis result instead.
    """

    messages = response["messages"]

    final_answer = messages[-1].content

    forbidden_terms = [
        "oee_analysis",
        "downtime_analysis",
        "scrap_analysis",
        "error_analysis",
        "machine_performance",
        "root_cause_analysis",
        "tool call",
        "tool response",
        "used the tool",
        "used the `"
    ]

    has_internal_reference = any(
        term.lower() in final_answer.lower()
        for term in forbidden_terms
    )

    tool_messages = [
        message
        for message in messages
        if type(message).__name__ == "ToolMessage"
    ]

    if not tool_messages:
        return final_answer

    analysis_result = tool_messages[-1].content.strip()

    important_keywords = [
        "OEE",
        "Downtime",
        "Scrap",
        "occurrences",
        "Total Production",
        "Good Quantity"
    ]

    has_evidence_keyword = any(
        keyword.lower() in final_answer.lower()
        for keyword in important_keywords
    )

    answer_without_machine_ids = re.sub(
        r"\bM[1-4]\b",
        "",
        final_answer,
        flags=re.IGNORECASE
    )

    has_numeric_evidence = any(
        character.isdigit()
        for character in answer_without_machine_ids
    )

    final_has_evidence = (
        has_evidence_keyword
        and has_numeric_evidence
    )

    if has_internal_reference:
        return analysis_result

    if not final_has_evidence:
        return analysis_result

    return final_answer


# -----------------------------
# Test Agent
# -----------------------------

if __name__ == "__main__":

    questions = [
        "Which machine should be investigated first?"
    ]

    for question in questions:

        print("\n==============================")
        print("QUESTION:")
        print(question)
        print("==============================")

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

        print("\n--- MESSAGE TRACE ---")

        for index, message in enumerate(
            response["messages"]
        ):

            print("\nMESSAGE:", index)

            print(
                "TYPE:",
                type(message).__name__
            )

            print("CONTENT:")
            print(message.content)

            if hasattr(
                message,
                "tool_calls"
            ):

                print("TOOL CALLS:")
                print(message.tool_calls)

            print("--------------------")

        print("\nFINAL ANSWER:")

        safe_answer = build_safe_final_answer(
            response
        )

        print(safe_answer)