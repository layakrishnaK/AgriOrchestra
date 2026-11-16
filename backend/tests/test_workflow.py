
"""
Automated tests for the AgriOrchestraAI workflow.

Tests the successful execution and failure handling
of the Soil, Market, and Advisory agents.
"""

import pytest

from backend.orchestrator import run_workflow


def test_successful_workflow():
    """All three agents should complete successfully."""

    result = run_workflow({
        "location": "Jaipur",
        "land_area": 2,
    })

    assert result["status"] == "completed"

    assert result["soil_result"]["status"] == "success"
    assert result["market_result"]["status"] == "success"
    assert result["advisory_result"]["status"] == "success"

    assert result["errors"] == []
    assert len(result["execution_trace"]) == 3
    assert result["request_id"]


@pytest.mark.parametrize(
    "failed_agent, expected_statuses",
    [
        (
            "soil_agent",
            ("failed", "success", "skipped"),
        ),
        (
            "market_agent",
            ("success", "failed", "skipped"),
        ),
        (
            "advisory_agent",
            ("success", "success", "failed"),
        ),
    ],
)
def test_agent_failure_handling(failed_agent, expected_statuses):
    """The workflow should record agent failures correctly."""

    result = run_workflow({
        "location": "Jaipur",
        "land_area": 2,
        "mock_fail_agents": [failed_agent],
    })

    soil_status, market_status, advisory_status = expected_statuses

    assert result["status"] == "failed"

    assert result["soil_result"]["status"] == soil_status
    assert result["market_result"]["status"] == market_status
    assert result["advisory_result"]["status"] == advisory_status

    assert len(result["errors"]) >= 1
    assert len(result["execution_trace"]) == 3
