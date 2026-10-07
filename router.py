import json
import re

import mlflow
from mlflow.entities import SpanType

from models import Route


SYSTEM_PROMPT = """Classify a research question for a system with exactly two specialist knowledge domains.

PYTHON: Python language, packaging, libraries, testing, concurrency, code, or Python application engineering.
DATABRICKS: Databricks platform, Unity Catalog, MLflow on Databricks, Delta Lake, Lakeflow, Databricks SQL, Vector Search, Model Serving, Databricks Apps, or Photon.
BOTH: answering well requires material knowledge from BOTH Python and Databricks.
UNSUPPORTED: neither domain can ground the answer.

Return JSON only:
{"route":"PYTHON|DATABRICKS|BOTH|UNSUPPORTED","reason":"one short sentence"}

Do not choose BOTH merely because Python can be used on Databricks. Choose BOTH only when the question actually asks about both domains.
"""


@mlflow.trace(span_type=SpanType.LLM, name="router_agent")
def route_query(client, model: str, query: str) -> tuple[Route, str]:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0,
        max_tokens=120,
    )
    raw = response.choices[0].message.content.strip()
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not match:
        return Route.UNSUPPORTED, "Router returned an invalid response."

    try:
        payload = json.loads(match.group(0))
        return Route(payload["route"].upper()), str(payload.get("reason", ""))
    except (json.JSONDecodeError, KeyError, ValueError):
        return Route.UNSUPPORTED, "Router returned an invalid response."
