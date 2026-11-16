
"""
LangGraph orchestrator for AgriOrchestraAI.

Coordinates the soil, market, and advisory agents.
The current implementation uses mock agents so the backend
can be developed independently of the actual agent implementations.
"""

from typing import Any, Dict

from langgraph.graph import END, START, StateGraph

from backend.state import AgricultureState, create_initial_state
from backend.mocks.mock_agents import (
    run_advisory_agent,
    run_market_agent,
    run_soil_agent,
)


def initialize_workflow(state: AgricultureState) -> Dict[str, Any]:
    """Mark the workflow as running."""

    return {"status": "running"}


def soil_node(state: AgricultureState) -> Dict[str, Any]:
    """Execute the Soil Agent."""

    try:
        return run_soil_agent(state)
    except Exception as exc:
        return {
            "soil_result": {
                "status": "failed",
                "data": {},
                "summary": "Soil agent execution failed.",
                "warnings": [],
                "error": str(exc),
            }
        }


def market_node(state: AgricultureState) -> Dict[str, Any]:
    """Execute the Market Agent."""

    try:
        return run_market_agent(state)
    except Exception as exc:
        return {
            "market_result": {
                "status": "failed",
                "data": {},
                "summary": "Market agent execution failed.",
                "warnings": [],
                "error": str(exc),
            }
        }


def advisory_node(state: AgricultureState) -> Dict[str, Any]:
    """Execute the Advisory Agent after both upstream agents finish."""

    try:
        return run_advisory_agent(state)
    except Exception as exc:
        return {
            "advisory_result": {
                "status": "failed",
                "data": {},
                "summary": "Advisory agent execution failed.",
                "warnings": [],
                "error": str(exc),
            }
        }


def finalize_workflow(state: AgricultureState) -> Dict[str, Any]:
    """
    Aggregate errors, record execution history,
    and determine the final workflow status.
    """

    soil_result = state.get("soil_result", {})
    market_result = state.get("market_result", {})
    advisory_result = state.get("advisory_result", {})

    results = [
        ("soil_agent", soil_result),
        ("market_agent", market_result),
        ("advisory_agent", advisory_result),
    ]

    execution_trace = []
    errors = []

    for agent_name, result in results:
        agent_status = result.get("status", "failed")
        execution_trace.append(f"{agent_name}: {agent_status}")

        if agent_status == "failed":
            error_message = result.get(
                "error",
                result.get("summary", "Unknown error"),
            )
            errors.append(f"{agent_name}: {error_message}")

    all_succeeded = all(
        result.get("status") == "success"
        for _, result in results
    )

    return {
        "execution_trace": execution_trace,
        "errors": errors,
        "status": "completed" if all_succeeded else "failed",
    }


def build_workflow():
    """Build and compile the LangGraph workflow."""

    workflow = StateGraph(AgricultureState)

    workflow.add_node("initialize", initialize_workflow)
    workflow.add_node("soil_agent", soil_node)
    workflow.add_node("market_agent", market_node)
    workflow.add_node("advisory_agent", advisory_node)
    workflow.add_node("finalize", finalize_workflow)

    workflow.add_edge(START, "initialize")

    # Soil and market analysis run as independent parallel branches.
    workflow.add_edge("initialize", "soil_agent")
    workflow.add_edge("initialize", "market_agent")

    # Advisory waits until BOTH upstream agents have finished.
    workflow.add_edge(
        ["soil_agent", "market_agent"],
        "advisory_agent",
    )

    workflow.add_edge("advisory_agent", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile()


def run_workflow(
    farmer_input: Dict[str, Any],
) -> AgricultureState:
    """
    Run the complete agricultural workflow.

    Args:
        farmer_input: Information received from the frontend.

    Returns:
        The final shared workflow state.
    """

    initial_state = create_initial_state(farmer_input)
    app = build_workflow()

    final_state = app.invoke(initial_state)

    return final_state
