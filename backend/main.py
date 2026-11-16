
"""
FastAPI application entry point for AgriOrchestraAI.

Exposes the LangGraph agricultural workflow through REST endpoints.
Currently uses mock agents through the backend orchestrator.
"""

from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from backend.orchestrator import run_workflow


app = FastAPI(
    title="AgriOrchestraAI Backend",
    description=(
        "Multi-agent agricultural advisory backend "
        "powered by LangGraph."
    ),
    version="1.0.0",
)


@app.get("/")
def root() -> Dict[str, str]:
    """Return basic API information."""

    return {
        "message": "Welcome to AgriOrchestraAI Backend",
        "status": "running",
    }


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Check backend availability."""

    return {
        "status": "healthy",
        "service": "AgriOrchestraAI",
    }


@app.post("/api/analyze")
def analyze_farmer_input(
    farmer_input: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Receive farmer information and execute the LangGraph workflow.

    The request body is passed directly to the orchestrator.
    """

    try:
        result = run_workflow(farmer_input)
        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the request.",
        )
