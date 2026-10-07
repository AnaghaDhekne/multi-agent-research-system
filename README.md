# Multi-Agent Research System

A routed, grounded research system built on Databricks. An LLM router delegates each question to specialized Python and/or Databricks research agents, and a synthesis agent produces a final answer strictly from retrieved specialist evidence.

This is the third stage of a three-project progression from lexical retrieval to semantic RAG and then explicit multi-agent orchestration.

## Architecture

```text
                         User question
                              |
                              v
                         Router Agent
                              |
              +---------------+---------------+
              |               |               |
           PYTHON        DATABRICKS          BOTH
              |               |               |
              v               v          +----+----+
      Python Specialist  Databricks       |         |
        Vector Search    Specialist       v         v
        + fallback       lexical KB     Python   Databricks
              |               |          agent     agent
              +---------------+-------------+-------+
                              |
                              v
                       Synthesis Agent
                              |
                              v
                    Evidence-grounded answer

UNSUPPORTED -> grounded refusal
```

For `BOTH` questions, the Python and Databricks specialists execute in parallel before their evidence is passed to synthesis.

## Agent responsibilities

### Router Agent

Classifies each request as:

- `PYTHON` — Python language/application engineering knowledge is required.
- `DATABRICKS` — Databricks platform knowledge is required.
- `BOTH` — material evidence from both domains is required.
- `UNSUPPORTED` — neither available knowledge domain can ground the answer.

The router is explicitly instructed not to select `BOTH` merely because Python can be used on Databricks.

### Python Specialist

Uses the semantic-retrieval capability developed in the Stage 2 RAG project. It queries the existing Databricks Vector Search index and falls back to a small local Python knowledge base if Vector Search is unavailable.

### Databricks Specialist

Performs lexical retrieval over a curated Databricks knowledge base covering Unity Catalog, MLflow, Delta Lake, Databricks SQL, Lakeflow Jobs, Vector Search, Model Serving, Auto Loader, Databricks Apps, Unity Catalog Volumes, and Photon.

### Synthesis Agent

Receives only the evidence returned by the selected specialists. It is instructed to answer from that evidence, cite evidence labels such as `[PYTHON-1]` and `[DATABRICKS-1]`, and identify insufficient evidence rather than filling gaps with unsupported information.

## Databricks capabilities demonstrated

- Foundation Model API for intelligent routing and synthesis
- Databricks Vector Search for semantic Python retrieval
- MLflow tracing across router, retrievers, synthesis, and orchestration
- Databricks Apps with Streamlit
- Reuse of a Unity Catalog-backed Vector Search index from the Stage 2 project
- Environment-configurable model and index settings
- Parallel specialist execution for cross-domain requests

## Project structure

```text
.
├── app.py
├── app.yaml
├── config.py
├── knowledge.py
├── models.py
├── orchestrator.py
├── router.py
├── specialists.py
├── eval_router.py
├── evals/
│   └── router_cases.json
└── requirements.txt
```

- `router.py` — intent classification
- `specialists.py` — specialist retrieval tools
- `orchestrator.py` — delegation, parallel execution, and evidence synthesis
- `models.py` — shared route/evidence contracts
- `knowledge.py` — local specialist knowledge and fallback data
- `config.py` — environment-based Databricks configuration
- `app.py` — Streamlit application
- `eval_router.py` — reproducible routing evaluation

## Project progression

**Stage 1 — [Research AI Assistant](https://github.com/AnaghaDhekne/research-ai-assistant)**  
Grounded Databricks assistant using lexical retrieval, Foundation Model access, Streamlit, and MLflow tracing.

**Stage 2 — [RAG Research Agent](https://github.com/AnaghaDhekne/rag-research-agent)**  
Adds semantic Vector Search, keyword fallback, AI Gateway/Foundation Model fallback, Unity Catalog inference logging, and richer observability.

**Stage 3 — Multi-Agent Research System (this repository)**  
Separates responsibilities into an LLM router, domain-specialized retrieval agents, parallel cross-domain execution, and a synthesis agent.

The progression is intentionally incremental: each repository introduces a distinct architectural capability rather than replacing the previous project with an unrelated demo.

## Evaluation

The repository includes labeled routing cases spanning:

- Python-only questions
- Databricks-only questions
- Cross-domain questions requiring both specialists
- Unsupported questions

Run:

```bash
python eval_router.py
```

The evaluator reports predicted vs. expected routes and overall routing accuracy. Measured results should be reported only after executing the evaluation in the target Databricks workspace.

A useful cross-domain test is:

> How should I package a Python RAG app and host it with Databricks Apps?

The expected route is `BOTH`: Python evidence is needed for packaging/application structure, while Databricks evidence is needed for the hosting platform.

## Run on Databricks

The default Python Vector Search index is:

```text
main.default.python_kb_docs_index
```

Resource names can be overridden with environment variables such as `PYTHON_VS_INDEX`, `ROUTER_MODEL`, and `SYNTHESIS_MODEL`.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

`app.yaml` configures the application for Databricks Apps on port 8000.

## Current scope

This is a focused v1 rather than an autonomous-agent framework. Agents have distinct responsibilities and tool boundaries, but there are no open-ended planning loops, autonomous tool discovery, or separate judge agent.

The current evaluation measures routing behavior. Future evaluation can compare dynamic routing against always-query-both and single-specialist baselines on groundedness, latency, token usage, and unnecessary specialist invocation.
