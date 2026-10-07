import mlflow
from mlflow.entities import SpanType

from config import PYTHON_VS_INDEX, PYTHON_VS_NUM_RESULTS
from knowledge import DATABRICKS_KB, PYTHON_FALLBACK_KB
from models import Evidence, SpecialistResult


def _keyword_search(query: str, documents: list[dict], source: str) -> list[Evidence]:
    words = {w.strip(".,?!:;()[]{}").lower() for w in query.split() if len(w) > 2}
    ranked = []
    for doc in documents:
        topic = doc["topic"].lower()
        content = doc["content"].lower()
        topic_words = set(topic.split())
        score = 4 * len(words & topic_words) + sum(1 for word in words if word in content)
        if score:
            ranked.append((score, doc))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [
        Evidence(source=source, topic=doc["topic"], content=doc["content"], score=float(score))
        for score, doc in ranked[:4]
    ]


@mlflow.trace(span_type=SpanType.RETRIEVER, name="databricks_specialist")
def databricks_specialist(query: str) -> SpecialistResult:
    evidence = _keyword_search(query, DATABRICKS_KB, "databricks_kb")
    return SpecialistResult(specialist="databricks", evidence=evidence)


@mlflow.trace(span_type=SpanType.RETRIEVER, name="python_specialist")
def python_specialist(workspace_client, query: str) -> SpecialistResult:
    evidence = []
    try:
        results = workspace_client.vector_search_indexes.query_index(
            index_name=PYTHON_VS_INDEX,
            columns=["id", "topic", "content"],
            query_text=query,
            num_results=PYTHON_VS_NUM_RESULTS,
        )
        if results.result and results.result.data_array:
            for row in results.result.data_array:
                evidence.append(
                    Evidence(
                        source="python_vector_search",
                        topic=str(row[1]),
                        content=str(row[2]),
                    )
                )
    except Exception:
        evidence = []

    if not evidence:
        evidence = _keyword_search(query, PYTHON_FALLBACK_KB, "python_fallback_kb")

    return SpecialistResult(specialist="python", evidence=evidence)
