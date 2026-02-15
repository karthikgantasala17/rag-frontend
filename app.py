import streamlit as st
import requests

BACKEND_URL = "https://karthikgantasala17-rag-fastapi-bot.hf.space"

st.set_page_config(page_title="RAG Chatbot", layout="centered")

st.title("📄 RAG Chatbot")
st.caption("Streamlit Frontend • FastAPI Backend")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Controls")

    if st.button("Reindex PDFs"):
        requests.post(f"{BACKEND_URL}/reindex")
        st.success("Reindexed")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask something about documents...")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    payload = {
        "question": question,
        "history": st.session_state.messages
    }

    res = requests.post(f"{BACKEND_URL}/ask", json=payload)

    if res.status_code == 200:
        answer = res.json()["answer"]
    else:
        answer = "Backend error"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})
