from concurrent.futures import ThreadPoolExecutor

import mlflow
from mlflow.entities import SpanType

from config import MAX_HISTORY_TURNS, ROUTER_MODEL, SYNTHESIS_MODEL
from models import Route, SpecialistResult
from router import route_query
from specialists import databricks_specialist, python_specialist


def _format_evidence(results: list[SpecialistResult]) -> str:
    blocks = []
    for result in results:
        for i, item in enumerate(result.evidence, start=1):
            blocks.append(f"[{result.specialist.upper()}-{i}] {item.topic}\n{item.content}")
    return "\n\n".join(blocks)


@mlflow.trace(span_type=SpanType.LLM, name="synthesis_agent")
def synthesize(client, model: str, query: str, results: list[SpecialistResult], history: list[tuple[str, str]]) -> str:
    evidence = _format_evidence(results)
    if not evidence:
        return "I couldn't find enough evidence in the available Python or Databricks knowledge sources to answer that reliably."

    history_text = "\n".join(
        f"User: {q}\nAssistant: {a}" for q, a in history[-MAX_HISTORY_TURNS:]
    ) if history else "(none)"

    prompt = f"""You are the synthesis agent in a grounded multi-agent research system.
Answer using ONLY the specialist evidence below.
Combine evidence across specialists when useful.
Do not invent facts absent from the evidence.
Cite claims inline using labels such as [PYTHON-1] and [DATABRICKS-1].
If evidence is insufficient, say what is missing.

Previous conversation:
{history_text}

Specialist evidence:
{evidence}

Question: {query}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=700,
    )
    return response.choices[0].message.content


@mlflow.trace(span_type=SpanType.CHAIN, name="multi_agent_orchestrator")
def answer_query(workspace_client, llm_client, query: str, history=None) -> dict:
    history = history or []
    route, reason = route_query(llm_client, ROUTER_MODEL, query)

    if route == Route.UNSUPPORTED:
        return {
            "route": route.value,
            "reason": reason,
            "answer": "This question is outside the currently grounded Python and Databricks knowledge domains.",
            "specialists": [],
        }

    if route == Route.PYTHON:
        results = [python_specialist(workspace_client, query)]
    elif route == Route.DATABRICKS:
        results = [databricks_specialist(query)]
    else:
        with ThreadPoolExecutor(max_workers=2) as pool:
            py_future = pool.submit(python_specialist, workspace_client, query)
            db_future = pool.submit(databricks_specialist, query)
            results = [py_future.result(), db_future.result()]

    answer = synthesize(llm_client, SYNTHESIS_MODEL, query, results, history)
    return {
        "route": route.value,
        "reason": reason,
        "answer": answer,
        "specialists": [r.specialist for r in results],
    }
