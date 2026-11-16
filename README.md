# AgriOrchestraAI

Multi-agent agricultural advisory backend powered by **FastAPI** and **LangGraph**.

## 1. Project Overview

AgriOrchestraAI coordinates three agricultural agents:

- **Soil Agent:** Soil analysis.
- **Market Agent:** Market intelligence.
- **Advisory Agent:** Agricultural recommendations based on soil and market results.

The backend currently uses mock agents for independent development and testing.

## 2. Technology Stack

- Python
- FastAPI
- LangGraph
- Uvicorn
- Pytest

## 3. Project Structure

```text
backend/
├── main.py
├── state.py
├── orchestrator.py
├── agents/
├── mocks/
│   └── mock_agents.py
├── rag/
└── tests/
    └── test_workflow.py

docs/
└── CONTRACT.md

requirements.txt
```

## 4. Setup Instructions

### Clone the repository

```bash
git clone https://github.com/layakrishnaK/AgriOrchestra.git
cd AgriOrchestra
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

Windows CMD:

```cmd
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

## 6. API Documentation

Interactive Swagger documentation:

`http://127.0.0.1:8000/docs`

Available endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend information |
| GET | `/health` | Health check |
| POST | `/api/analyze` | Execute agricultural workflow |

## 7. Example API Request

POST `/api/analyze`

```json
{
  "location": "Jaipur",
  "land_area": 2
}
```

The response contains:

- Request ID
- Farmer input
- Soil analysis result
- Market intelligence result
- Advisory result
- Execution trace
- Errors
- Workflow status

## 8. Automated Testing

Run the workflow tests:

```bash
python -m pytest backend/tests/test_workflow.py -v
```

The tests cover:

1. Successful workflow execution.
2. Soil Agent failure.
3. Market Agent failure.
4. Advisory Agent failure.

## 9. Workflow Execution

1. Initialize shared agricultural state.
2. Execute Soil and Market agents in parallel.
3. Execute Advisory Agent after both upstream agents finish.
4. Aggregate results and errors.
5. Return the final workflow state.

## 10. Development Status

**Current status:** Backend foundation implemented and tested with mock agents.

Actual agricultural agent implementations and frontend integration are separate development responsibilities.

See `docs/CONTRACT.md` for the shared state structure and agent integration requirements.