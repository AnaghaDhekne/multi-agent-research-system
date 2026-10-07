DATABRICKS_KB = [
    {"topic": "Unity Catalog", "content": "Unity Catalog is Databricks' unified governance solution for data and AI assets. It provides centralized access control, auditing, lineage tracking, and data discovery."},
    {"topic": "MLflow Tracing", "content": "MLflow Tracing records execution of GenAI applications, including LLM calls, retrievers, chains, inputs, outputs, metadata, and timing."},
    {"topic": "Delta Lake", "content": "Delta Lake is an open-source storage layer that adds ACID transactions, schema enforcement, time travel, and unified batch and streaming processing."},
    {"topic": "Databricks SQL", "content": "Databricks SQL provides SQL warehouses, a SQL editor, query history, dashboards, and alerts for querying lakehouse data."},
    {"topic": "Lakeflow Jobs", "content": "Lakeflow Jobs orchestrates notebooks, Python scripts, SQL queries, and pipelines with DAGs, retries, conditions, and triggers."},
    {"topic": "Vector Search", "content": "Databricks Vector Search is a similarity-search service for vector embeddings and supports RAG applications and Delta table synchronization."},
    {"topic": "Model Serving", "content": "Databricks Model Serving provides serverless real-time inference for foundation models, external models, and custom models."},
    {"topic": "Auto Loader", "content": "Auto Loader incrementally processes new files from cloud storage with schema inference and evolution."},
    {"topic": "Databricks Apps", "content": "Databricks Apps hosts data and AI applications and supports frameworks including Streamlit, Flask, FastAPI, and Gradio."},
    {"topic": "MLflow", "content": "MLflow manages the ML lifecycle and includes experiment tracking, model registry, deployment, evaluation, and GenAI tracing."},
    {"topic": "Unity Catalog Volumes", "content": "Unity Catalog Volumes provide governed storage for non-tabular files inside Unity Catalog."},
    {"topic": "Photon", "content": "Photon is Databricks' native vectorized query engine for accelerating SQL and DataFrame workloads."},
]

# Small local fallback. In Databricks, the Python specialist first queries the
# existing Vector Search index created by the predecessor RAG project.
PYTHON_FALLBACK_KB = [
    {"topic": "Python Packaging", "content": "Modern Python packages commonly use pyproject.toml. Virtual environments isolate dependencies, and pip install -e . supports editable local installs."},
    {"topic": "Python Virtual Environments", "content": "Create an isolated environment with python -m venv .venv and install dependencies from requirements.txt or project metadata."},
    {"topic": "Python AsyncIO", "content": "asyncio supports cooperative concurrency using async def and await and is useful for I/O-bound workloads."},
    {"topic": "Python Testing", "content": "pytest supports plain assertions, fixtures, parametrization, markers, and plugins such as pytest-cov."},
    {"topic": "Python Logging", "content": "The logging module provides leveled application logging through loggers, handlers, and formatters."},
]
