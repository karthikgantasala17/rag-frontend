import streamlit as st
import requests

BACKEND_URL = "https://karthikgantasala17-rag-fastapi-bot.hf.space"

st.set_page_config(page_title="RAG Chatbot", layout="centered")

st.title("📄 RAG Chatbot")
st.caption("Streamlit Frontend • FastAPI Backend")

# ----------------------------------
# Session state
# ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# Sidebar
# ----------------------------------
with st.sidebar:
    st.header("Controls")

    if st.button("🔄 Reindex PDFs"):
        requests.post(f"{BACKEND_URL}/reindex")
        st.success("Reindexed")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------
# Display history
# ----------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------------
# Input
# ----------------------------------
question = st.chat_input("Ask something about documents...")

if question:

    # Greeting
    if question.lower().strip() in ["hi", "hello", "hey"]:
        greeting = "Hello! Ask me a question about the documents 🙂"

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": greeting}
        )

        st.rerun()

    # User message
    with st.chat_message("user"):
        st.markdown(question)

    payload = {
        "question": question,
        "history": st.session_state.messages
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                res = requests.post(
                    f"{BACKEND_URL}/ask",
                    json=payload,
                    timeout=60
                )

                if res.status_code == 200:
                    data = res.json()
                
                    answer = data.get("answer", "")
                    sources = data.get("sources", [])
                
                    st.markdown(answer)
                
                    if sources:
                        st.caption("Sources:")
                        for s in sources:
                            st.write(f"- {s['file']} (page {s['page']})")
                else:
                    st.error("Backend error")

            except Exception as e:
                st.error(str(e))

    # Save messages
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
