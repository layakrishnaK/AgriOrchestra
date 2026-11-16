# AgriOrchestraAI — Backend API & Agent Contract

**Version:** 1.0  
**Status:** Initial development contract  
**Purpose:** Define communication standards between the frontend, backend orchestrator and agricultural agents.

---

## 1. System Overview

AgriOrchestraAI is a multi-agent agricultural advisory system.

The backend coordinates three specialized agents:

1. **Soil Agent:** Analyses soil information and produces soil-related insights.
2. **Market Agent:** Retrieves and analyses agricultural market information.
3. **Advisory Agent:** Combines soil and market results to produce agricultural recommendations.

The LangGraph orchestrator manages execution and shared state.

### Workflow

Farmer Input → Orchestrator → Soil Agent + Market Agent → Advisory Agent → Final Output

Soil analysis and market intelligence are independent stages. The advisory stage consumes their results.

---

## 2. Shared State Definition

The shared state is defined in `backend/state.py` using Python `TypedDict`.

### AgricultureState

| Field | Data Type | Description |
|---|---|---|
| request_id | str | Unique request identifier |
| farmer_input | Dict[str, Any] | Information received from frontend |
| soil_result | Dict[str, Any] | Soil analysis output |
| market_result | Dict[str, Any] | Market intelligence output |
| advisory_result | Dict[str, Any] | Final agricultural advisory |
| execution_trace | List[str] | Records agent execution |
| errors | List[str] | Records workflow errors |
| status | Literal | Current workflow status |

### Allowed workflow statuses

- `pending` — Request created but not started.
- `running` — Workflow is executing.
- `completed` — Workflow completed successfully.
- `failed` — Workflow encountered a fatal error.

### Initial State

The function `create_initial_state()` initializes the shared state with:

- A unique request ID.
- Farmer input.
- Empty agent result dictionaries.
- Empty execution trace.
- Empty error list.
- Status set to `pending`.

---

## 3. Farmer Input Contract

The frontend sends farmer information through the backend.

The initial input is represented as:

```python
{
    "location": "Jaipur",
    "land_area": 2
}
```

This is an illustrative example, not the finalized frontend schema.

Additional fields may include:

- Farm location.
- Land area and measurement unit.
- Soil parameters.
- Crop preferences.
- Irrigation information.
- Farming requirements.

Exact field names, units, validation rules and default values will be finalized when the frontend contract is available.

The backend must not assume that optional fields are always present.

---

## 4. Agent Interface Contract

All agents must follow a common adapter interface:

```python
def run(state: AgricultureState) -> dict:
    """
    Execute the agent using the shared workflow state.

    Returns:
        A dictionary containing only the state updates.
    """
```

Agents must:

- Accept the shared state as input.
- Read only the information required for their task.
- Return structured dictionary updates.
- Avoid directly modifying the original state.
- Record their execution through the orchestrator.
- Report failures clearly.

The orchestrator is responsible for merging returned updates into the shared state.

### 4.1 Soil Agent

**File:** `backend/agents/soil_agent.py`

**Responsibility:**

Analyse available soil information and return soil-related insights.

**Input:**

- Farmer information.
- Available soil parameters.
- Relevant soil data, when available.

**Output field:** `soil_result`

Expected structure:

```python
{
    "status": "success",
    "data": {},
    "summary": "Soil analysis completed.",
    "warnings": []
}
```

The `data` dictionary will contain the actual soil-analysis fields agreed upon with the soil agent implementation owner.

### 4.2 Market Agent

**File:** `backend/agents/market_agent.py`

**Responsibility:**

Analyse agricultural market information and provide relevant market insights.

**Input:**

- Farmer location.
- Crop information, when available.
- Relevant market and mandi information.

**Output field:** `market_result`

Expected structure:

```python
{
    "status": "success",
    "data": {},
    "summary": "Market analysis completed.",
    "warnings": []
}
```

The `data` dictionary will contain market-specific information such as crop prices, mandi details and relevant trends when available.

### 4.3 Advisory Agent

**File:** `backend/agents/advisory_agent.py`

**Responsibility:**

Generate agricultural recommendations using the available soil and market information.

**Input:**

- Farmer information.
- Soil agent results.
- Market agent results.

**Output field:** `advisory_result`

Expected structure:

```python
{
    "status": "success",
    "data": {},
    "summary": "Agricultural advisory generated.",
    "warnings": []
}
```

The advisory agent must clearly distinguish between available data, assumptions and recommendations.

---

## 5. Standard Agent Output Format

All agent result dictionaries follow a common envelope:

| Field | Type | Description |
|---|---|---|
| status | str | Agent execution status |
| data | dict | Agent-specific output |
| summary | str | Brief explanation |
| warnings | list[str] | Limitations or warnings |

Allowed agent result statuses:

- `success`
- `failed`
- `skipped`

Agent-specific information belongs inside `data`.

This standard format allows the orchestrator to process different agent outputs consistently.

---

## 6. Execution Trace Contract

The orchestrator maintains an execution history through `execution_trace`.

Example:

```python
[
    "soil_agent: completed",
    "market_agent: completed",
    "advisory_agent: completed"
]
```

Each entry records an agent execution event.

The trace helps identify which stages executed and where a failure occurred.

---

## 7. Error Handling Contract

Errors are recorded in the shared `errors` list.

Example:

```python
{
    "errors": [
        "market_agent: Market data unavailable"
    ],
    "status": "failed"
}
```

Error-handling rules:

1. Agent failures must be reported to the orchestrator.
2. The orchestrator records the error.
3. Fatal workflow failures set the workflow status to `failed`.
4. Failed or unavailable agent results must not be treated as successful results.
5. Advisory generation must not proceed when required upstream information is unavailable.
6. Error messages must be clear and must not expose API keys or credentials.

---

## 8. Workflow Execution Contract

The orchestrator follows this logical execution sequence:

1. Receive farmer input.
2. Initialize shared state.
3. Set workflow status to `running`.
4. Execute soil analysis and market intelligence independently.
5. Store both agent results in shared state.
6. Verify that required upstream results are available.
7. Execute the advisory agent.
8. Store the final advisory.
9. Update execution trace and workflow status.
10. Return the final shared state.

### Completion

If all required stages succeed:

```python
status = "completed"
```

### Failure

If a required stage fails:

```python
status = "failed"
```

The orchestrator must not report successful completion when required stages have failed.

---

## 9. Mock Agent Contract

During independent backend development, mock agents will simulate the three specialized agents.

**Location:** `backend/mocks/mock_agents.py`

Mock agents must:

- Follow the same interface as actual agent adapters.
- Accept the shared state.
- Return the standard output structure.
- Produce deterministic sample responses.
- Clearly identify simulated results as mock data.
- Support testing of successful and failed execution paths.

Mock responses are for development and testing only. They must not be represented as verified agricultural recommendations or live market information.

---

## 10. Project File Responsibilities

| File | Responsibility |
|---|---|
| `backend/state.py` | Shared workflow state |
| `backend/orchestrator.py` | LangGraph workflow coordination |
| `backend/main.py` | Application entry point |
| `backend/mocks/mock_agents.py` | Mock agent implementations |
| `backend/agents/soil_agent.py` | Soil analysis agent |
| `backend/agents/market_agent.py` | Market intelligence agent |
| `backend/agents/advisory_agent.py` | Agricultural advisory agent |
| `backend/tests/` | Backend tests |
| `docs/CONTRACT.md` | Shared API and agent contract |

---

## 11. Integration Rules

1. All backend components must follow the shared state definition.
2. Agent adapters must follow the common `run(state)` interface.
3. Agent results must use the standard output envelope.
4. The orchestrator owns workflow status, error aggregation and execution trace management.
5. Actual agent implementations may use different internal technologies, but their adapters must satisfy this contract.
6. Changes to shared fields or output formats must be reflected in this document.
7. Mock implementations must remain replaceable without requiring changes to the overall workflow architecture.

---

**End of Contract**