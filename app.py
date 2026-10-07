import mlflow
import streamlit as st
from databricks.sdk import WorkspaceClient

from orchestrator import answer_query


st.set_page_config(page_title="Multi-Agent Research System", page_icon="🧭", layout="wide")
st.title("Multi-Agent Research System")
st.caption("A routed research assistant with specialized Python and Databricks agents.")

mlflow.set_tracking_uri("databricks")
try:
    mlflow.set_experiment("multi_agent_research_system")
except Exception:
    pass

w = WorkspaceClient()
llm_client = w.serving_endpoints.get_open_ai_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("route"):
            st.caption(f"Route: {message['route']} · Specialists: {', '.join(message.get('specialists', [])) or 'none'}")

if prompt := st.chat_input("Ask a Python, Databricks, or cross-domain question…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = []
    user_messages = [m for m in st.session_state.messages[:-1] if m["role"] == "user"]
    assistant_messages = [m for m in st.session_state.messages if m["role"] == "assistant"]
    for user_msg, assistant_msg in zip(user_messages, assistant_messages):
        history.append((user_msg["content"], assistant_msg["content"]))

    with st.chat_message("assistant"):
        with st.spinner("Routing to specialist agents…"):
            try:
                result = answer_query(w, llm_client, prompt, history)
                answer = result["answer"]
            except Exception as exc:
                result = {"route": "ERROR", "specialists": []}
                answer = f"⚠️ Error: {exc}"

        st.markdown(answer)
        st.caption(
            f"Route: {result['route']} · Specialists: "
            f"{', '.join(result.get('specialists', [])) or 'none'}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "route": result["route"],
            "specialists": result.get("specialists", []),
        }
    )

with st.sidebar:
    st.header("Architecture")
    st.markdown("**Router** → Python / Databricks / Both / Unsupported")
    st.markdown("**Python specialist** → Vector Search with local fallback")
    st.markdown("**Databricks specialist** → grounded domain retrieval")
    st.markdown("**Synthesis agent** → evidence-only final response")
    st.markdown("**Observability** → MLflow tracing")
