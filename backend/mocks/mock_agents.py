
"""
Mock implementations of the AgriOrchestraAI agents.

These agents allow the backend orchestrator to be developed
and tested independently of the actual agent implementations.

All responses generated here are simulated and must not be
treated as real agricultural advice or live market information.
"""

from typing import Any, Dict

from backend.state import AgricultureState


def _should_fail(state: AgricultureState, agent_name: str) -> bool:
    """
    Check whether a mock failure has been requested.

    Add an agent name to farmer_input["mock_fail_agents"]
    to simulate that agent failing during execution.
    """

    farmer_input = state.get("farmer_input", {})
    failed_agents = farmer_input.get("mock_fail_agents", [])

    if not isinstance(failed_agents, (list, tuple)):
        return False

    return agent_name in failed_agents


def _build_result(
    agent_name: str,
    message: str,
    status: str = "success",
) -> Dict[str, Any]:
    """Build a result using the standard agent output format."""

    return {
        "status": status,
        "data": {
            "mock": True,
            "agent": agent_name,
            "message": message,
        },
        "summary": message,
        "warnings": [
            "This is simulated mock data for development and testing only."
        ],
    }


def run_soil_agent(state: AgricultureState) -> Dict[str, Any]:
    """
    Simulate the Soil Agent.

    Returns:
        A partial state update containing soil_result.
    """

    if _should_fail(state, "soil_agent"):
        result = _build_result(
            agent_name="soil_agent",
            message="Simulated soil analysis failure.",
            status="failed",
        )
    else:
        result = _build_result(
            agent_name="soil_agent",
            message="Mock soil analysis completed. No real soil data was analysed.",
        )

    return {"soil_result": result}


def run_market_agent(state: AgricultureState) -> Dict[str, Any]:
    """
    Simulate the Market Agent.

    Returns:
        A partial state update containing market_result.
    """

    if _should_fail(state, "market_agent"):
        result = _build_result(
            agent_name="market_agent",
            message="Simulated market intelligence failure.",
            status="failed",
        )
    else:
        result = _build_result(
            agent_name="market_agent",
            message="Mock market analysis completed. No live mandi data was retrieved.",
        )

    return {"market_result": result}


def run_advisory_agent(state: AgricultureState) -> Dict[str, Any]:
    """
    Simulate the Advisory Agent.

    Advisory generation requires successful soil and market results.

    Returns:
        A partial state update containing advisory_result.
    """

    soil_result = state.get("soil_result", {})
    market_result = state.get("market_result", {})

    if (
        soil_result.get("status") != "success"
        or market_result.get("status") != "success"
    ):
        result = _build_result(
            agent_name="advisory_agent",
            message="Advisory generation skipped because required upstream results are unavailable.",
            status="skipped",
        )

        result["warnings"].append(
            "Both soil and market agents must succeed before advisory generation."
        )

        return {"advisory_result": result}

    if _should_fail(state, "advisory_agent"):
        result = _build_result(
            agent_name="advisory_agent",
            message="Simulated advisory generation failure.",
            status="failed",
        )
    else:
        result = _build_result(
            agent_name="advisory_agent",
            message="Mock advisory generated using simulated soil and market results. This is not a real farming recommendation.",
        )

    return {"advisory_result": result}
