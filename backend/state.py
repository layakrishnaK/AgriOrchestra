
"""
Shared state definition for AgriOrchestraAI.

This state is passed between the soil, market, and advisory
agents through the LangGraph orchestrator.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict
from uuid import uuid4


class AgricultureState(TypedDict, total=False):
    """
    Shared state used throughout the agricultural workflow.

    total=False allows individual LangGraph nodes to return
    only the fields they update.
    """

    # Request information
    request_id: str
    farmer_input: Dict[str, Any]

    # Agent outputs
    soil_result: Dict[str, Any]
    market_result: Dict[str, Any]
    advisory_result: Dict[str, Any]

    # Workflow management
    execution_trace: List[str]
    errors: List[str]
    status: Literal["pending", "running", "completed", "failed"]


def create_initial_state(
    farmer_input: Dict[str, Any],
    request_id: Optional[str] = None
) -> AgricultureState:
    """
    Create the initial state for a new farmer request.

    Args:
        farmer_input: Information received from the frontend.
        request_id: Optional unique request identifier.

    Returns:
        AgricultureState: Initialized workflow state.
    """

    return AgricultureState(
        request_id=request_id or str(uuid4()),
        farmer_input=dict(farmer_input),
        soil_result={},
        market_result={},
        advisory_result={},
        execution_trace=[],
        errors=[],
        status="pending"
    )
