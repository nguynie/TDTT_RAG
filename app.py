import streamlit as st

from config import CHAT_MODEL, EMBEDDING_MODEL, OLLAMA_BASE_URL, TOP_K
from firebase_client import FirebaseError, create_account, sign_in, validate_firebase_config
from rag import (
    RAGError,
    generate_rag_answer,
    index_knowledge_base,
    load_knowledge_base,
    retrieve_relevant_entries,
)

st.set_page_config(
    page_title="Lumen Travel Assistant - Ho Chi Minh City",
    layout="wide",
)


def forget_user():
    """Clear user session state and chat history."""
    for key in (
        "user",
        "chat_history",
        "auth_email",
        "auth_password",
        "auth_notice",
        "auth_error",
        "clear_password",
        "account_created",
    ):
        st.session_state.pop(key, None)


@st.cache_resource(show_spinner="Embedding travel guide entries...")
def get_cached_indexed_kb():
    """Embed travel guide once using st.cache_resource."""
    kb = load_knowledge_base("knowledge_base.json")
    return index_knowledge_base(kb, base_url=OLLAMA_BASE_URL)


def render_auth_page():
    st.markdown("<h2 style='text-align: center;'>Lumen Travel Assistant</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: gray;'>Ho Chi Minh City Travel Assistant with RAG Chat</p>",
        unsafe_allow_html=True,
    )

    try:
        validate_firebase_config()
    except FirebaseError as err:
        st.warning(f"Firebase configuration warning: {err}")
        st.info("Copy .env.example to .env and configure FIREBASE_PROJECT_ID and FIREBASE_API_KEY.")
        st.stop()

    if st.session_state.pop("clear_password", False):
        st.session_state["auth_password"] = ""
    if st.session_state.pop("account_created", False):
        st.success("Account created successfully. You can now sign in.")
    if "auth_error" in st.session_state:
        st.error(st.session_state.pop("auth_error"))
    if "auth_notice" in st.session_state:
        st.info(st.session_state.pop("auth_notice"))

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Account Sign In")
            st.caption("Only authenticated users can access the travel assistant.")

            with st.form("auth_form", clear_on_submit=False):
                email = st.text_input("Email", key="auth_email", placeholder="user@example.com")
                password = st.text_input("Password", type="password", key="auth_password", placeholder="Minimum 6 characters")

                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    login_btn = st.form_submit_button("Sign In", use_container_width=True)
                with c_btn2:
                    register_btn = st.form_submit_button("Sign Up", use_container_width=True)

            if register_btn:
                try:
                    create_account(email, password)
                    st.session_state["account_created"] = True
                    st.session_state["clear_password"] = True
                    st.rerun()
                except FirebaseError as e:
                    st.session_state["auth_error"] = str(e)
                    st.session_state["clear_password"] = True
                    st.rerun()

            elif login_btn:
                try:
                    user_data = sign_in(email, password)
                    forget_user()
                    st.session_state["user"] = user_data
                    st.session_state["chat_history"] = []
                    st.rerun()
                except FirebaseError as e:
                    st.session_state["auth_error"] = str(e)
                    st.session_state["clear_password"] = True
                    st.rerun()


def render_chat_page():
    user = st.session_state["user"]

    with st.sidebar:
        st.markdown("### Account")
        st.write(f"**Email:** `{user['email']}`")
        st.caption(f"UID: {user['uid']}")

        if st.button("Sign Out", use_container_width=True):
            forget_user()
            st.rerun()

        st.divider()
        st.markdown("### RAG Settings")
        st.markdown("- **City:** Ho Chi Minh City")
        st.markdown(f"- **Embedding:** `{EMBEDDING_MODEL}`")
        st.markdown(f"- **Chat Model:** `{CHAT_MODEL}`")
        st.markdown(f"- **Top-K:** `{TOP_K}`")
        st.markdown(f"- **Ollama URL:** `{OLLAMA_BASE_URL}`")

        st.divider()
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

    st.title("Lumen Travel Assistant - Ho Chi Minh City")
    st.caption("Factual travel assistant answering strictly from the verified travel guide.")

    try:
        indexed_kb = get_cached_indexed_kb()
    except (RAGError, Exception) as e:
        st.error(f"Cannot initialize RAG knowledge base: {e}")
        st.info("Ensure Ollama server is running and OLLAMA_BASE_URL is set in .env.")
        st.stop()

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("retrieved"):
                with st.expander("Retrieved Travel Guide References & Scores (Top-K)"):
                    for entry, score in msg["retrieved"]:
                        st.markdown(
                            f"**[{entry['id']}] {entry['title']}** (Category: `{entry.get('category', 'general')}`) - "
                            f"Cosine Similarity: `{score:.4f}`\n\n"
                            f"> {entry['text']}\n\n"
                            f"*Source: {entry.get('source', 'Lumen Travel')}*"
                        )
                        st.divider()

    user_query = st.chat_input("Ask about opening hours, ticket prices, locations in Ho Chi Minh City...")

    if user_query:
        query_text = user_query.strip()
        if not query_text:
            st.warning("Please enter a question.")
            return

        st.session_state["chat_history"].append({"role": "user", "content": query_text})
        with st.chat_message("user"):
            st.markdown(query_text)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving knowledge base entries..."):
                try:
                    retrieved_results = retrieve_relevant_entries(
                        query=query_text,
                        indexed_kb=indexed_kb,
                        base_url=OLLAMA_BASE_URL,
                        top_k=TOP_K,
                    )

                    answer = generate_rag_answer(
                        query=query_text,
                        retrieved_entries=retrieved_results,
                        base_url=OLLAMA_BASE_URL,
                        chat_model=CHAT_MODEL,
                    )

                    st.markdown(answer)

                    if retrieved_results:
                        with st.expander("Retrieved Travel Guide References & Scores (Top-K)"):
                            for entry, score in retrieved_results:
                                st.markdown(
                                    f"**[{entry['id']}] {entry['title']}** (Category: `{entry.get('category', 'general')}`) - "
                                    f"Cosine Similarity: `{score:.4f}`\n\n"
                                    f"> {entry['text']}\n\n"
                                    f"*Source: {entry.get('source', 'Lumen Travel')}*"
                                )
                                st.divider()

                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": answer,
                        "retrieved": retrieved_results,
                    })

                except RAGError as err:
                    st.error(f"RAG Error: {err}")
                except Exception as ex:
                    st.error(f"Unexpected error: {ex}")


if "user" not in st.session_state:
    render_auth_page()
else:
    render_chat_page()
