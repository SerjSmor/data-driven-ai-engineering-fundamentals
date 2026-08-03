import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def state_for(milestone, progress):
    required = [t for t in milestone["tasks"] if not t.get("optional")]
    states = [progress["tasks"][t["id"]]["status"] for t in required]
    if states and all(value == "complete" for value in states):
        return "complete"
    if any(value != "pending" for value in states):
        return "in progress"
    return "pending"


st.set_page_config(page_title="BuildGuild · Knowledge Base Chatbot", page_icon="📚", layout="wide")
st.title("Knowledge Base Chatbot with WixQA")
challenge, progress = load("challenge.json"), load("progress.json")
st.write(challenge["goal"])
st.caption("Retrieve evidence first. Answer second. Evaluate both stages.")

with st.expander("Dataset", expanded=True):
    st.markdown(f"[{challenge['dataset']['name']}]({challenge['dataset']['url']}) · `{challenge['dataset']['huggingface_id']}`")
    st.code(challenge["dataset"]["loading_example"], language="python")
    for note in challenge["dataset"]["notes"]:
        st.markdown(f"- {note}")

tabs = st.tabs([m["title"] for m in challenge["milestones"]])
for tab, milestone in zip(tabs, challenge["milestones"]):
    with tab:
        st.subheader(milestone["title"])
        st.caption(f"Status: {state_for(milestone, progress)}")
        st.markdown(milestone["long_description"])
        for task in milestone["tasks"]:
            task_state = progress["tasks"][task["id"]]["status"]
            optional = " · bonus" if task.get("optional") else ""
            with st.expander(f"{task['title']} · {task_state}{optional}"):
                st.write(task["full_explanation"])
                if task.get("small_hint"):
                    st.info(task["small_hint"])
                st.markdown("Expected artifacts:")
                for artifact in task.get("expected_artifacts", []):
                    st.code(artifact)
                st.caption(f"Task ID: {task['id']} · Judge level: {task.get('judge_level', 'medium')}")
