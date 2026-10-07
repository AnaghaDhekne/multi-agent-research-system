import json

from databricks.sdk import WorkspaceClient

from config import ROUTER_MODEL
from router import route_query


def main():
    w = WorkspaceClient()
    client = w.serving_endpoints.get_open_ai_client()

    with open("evals/router_cases.json", encoding="utf-8") as handle:
        cases = json.load(handle)

    correct = 0
    for case in cases:
        route, reason = route_query(client, ROUTER_MODEL, case["query"])
        passed = route.value == case["expected"]
        correct += int(passed)
        print(
            f"{'PASS' if passed else 'FAIL'} | expected={case['expected']:<11} "
            f"actual={route.value:<11} | {case['query']} | {reason}"
        )

    accuracy = correct / len(cases)
    print(f"\nRouter accuracy: {correct}/{len(cases)} = {accuracy:.1%}")


if __name__ == "__main__":
    main()
