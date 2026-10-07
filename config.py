import os

ROUTER_MODEL = os.getenv("ROUTER_MODEL", "databricks-meta-llama-3-3-70b-instruct")
SYNTHESIS_MODEL = os.getenv("SYNTHESIS_MODEL", ROUTER_MODEL)
PYTHON_VS_INDEX = os.getenv("PYTHON_VS_INDEX", "main.default.python_kb_docs_index")
PYTHON_VS_NUM_RESULTS = int(os.getenv("PYTHON_VS_NUM_RESULTS", "3"))
MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", "5"))
