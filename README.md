# Multi-Agent Research System

A routed, grounded research assistant built on Databricks. The system uses an LLM router to delegate questions to specialized Python and Databricks research agents, then synthesizes their evidence into one cited response.

## Architecture

```text
User question
     |
Router Agent
     |
 +---+-------------------+
 |                       |
Python Specialist   Databricks Specialist
Vector Search       Keyword retrieval
 |                       |
 +-----------+-----------+
             |
      Synthesis Agent
             |
      Grounded answer
```

The router selects `PYTHON`, `DATABRICKS`, `BOTH`, or `UNSUPPORTED`. Cross-domain questions invoke both specialists in parallel.

## Databricks features demonstrated

- Foundation Model API for routing and synthesis
- Databricks Vector Search for semantic Python retrieval
- MLflow tracing for router, retrievers, synthesis, and orchestration
- Databricks Apps + Streamlit UI
- Unity Catalog-backed Vector Search index inherited from the predecessor RAG project
- Environment-configurable resource names instead of workspace-specific IDs in source code

## Project lineage

This project evolves two earlier research assistants:

1. `research-ai-assistant` — Databricks-focused grounded assistant with keyword retrieval.
2. `rag-research-agent` — Python RAG assistant with Vector Search, AI Gateway/fallback, inference logging, and MLflow tracing.
3. `multi-agent-research-system` — intent routing, specialist delegation, parallel cross-domain retrieval, and evidence synthesis.

## Files

- `app.py` — Streamlit UI and Databricks client setup
- `router.py` — LLM-based intent router
- `specialists.py` — Python and Databricks retrieval specialists
- `orchestrator.py` — delegation, parallel execution, and synthesis
- `models.py` — shared route/evidence contracts
- `knowledge.py` — Databricks KB and Python fallback KB
- `config.py` — environment-based configuration
- `eval_router.py` — router evaluation runner
- `evals/router_cases.json` — labeled routing test set

## Run on Databricks

The default Python Vector Search index is:

```text
main.default.python_kb_docs_index
```

Override it with the `PYTHON_VS_INDEX` environment variable if needed.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

For Databricks Apps, `app.yaml` starts Streamlit on port 8000.

## Evaluate routing

```bash
python eval_router.py
```

The initial evaluation set covers Python-only, Databricks-only, cross-domain, and unsupported questions. Report measured accuracy only after running the evaluation in the target Databricks workspace.

## Example cross-domain question

> How should I package a Python RAG app and host it with Databricks Apps?

The router should select `BOTH`, retrieve evidence from both specialists, and synthesize one grounded answer with evidence labels.

## Current scope

This is intentionally a focused v1. It does not use autonomous agent loops or an external orchestration framework. Each agent has a distinct responsibility and tool boundary, making routing and retrieval behavior straightforward to trace and evaluate.
