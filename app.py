"""Streamlit Application: Sign-in Travel Assistant with RAG Chat (TP.HCM).
Combines Firebase Authentication and Ollama RAG.
"""

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

# Page configuration
st.set_page_config(
    page_title="Lumen Travel Assistant - TP.HCM",
    page_icon="🏙️",
    layout="wide",
)


# ---------------------------------------------------------
# Session & Cache Management
# ---------------------------------------------------------

def forget_user():
    """Clear session data for the current user and wipe chat history."""
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


@st.cache_resource(show_spinner="Đang đọc và nhúng cẩm nang du lịch TP.HCM vào bộ nhớ...")
def get_cached_indexed_kb():
    """Embed the travel guide once using @st.cache_resource."""
    kb = load_knowledge_base("knowledge_base.json")
    return index_knowledge_base(kb, base_url=OLLAMA_BASE_URL)


# ---------------------------------------------------------
# Authentication Screen
# ---------------------------------------------------------

def render_auth_page():
    st.markdown("<h2 style='text-align: center;'>🏙️ Lumen Travel Assistant</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: gray;'>Trợ lý du lịch thông minh TP. Hồ Chí Minh với công nghệ RAG</p>",
        unsafe_allow_html=True,
    )

    try:
        validate_firebase_config()
    except FirebaseError as err:
        st.warning(f"⚠️ Cấu hình Firebase: {err}")
        st.info("💡 Vui lòng sao chép `.env.example` sang `.env` và điền `FIREBASE_PROJECT_ID`, `FIREBASE_API_KEY`.")
        st.stop()

    # Flash messages
    if st.session_state.pop("clear_password", False):
        st.session_state["auth_password"] = ""
    if st.session_state.pop("account_created", False):
        st.success("Tạo tài khoản thành công! Bạn có thể đăng nhập ngay.")
    if "auth_error" in st.session_state:
        st.error(st.session_state.pop("auth_error"))
    if "auth_notice" in st.session_state:
        st.info(st.session_state.pop("auth_notice"))

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Đăng nhập tài khoản")
            st.caption("Chỉ người dùng đã đăng nhập mới có quyền sử dụng trợ lý RAG Chat.")

            with st.form("auth_form", clear_on_submit=False):
                email = st.text_input("Email", key="auth_email", placeholder="vidu@student.hcmus.edu.vn")
                password = st.text_input("Mật khẩu", type="password", key="auth_password", placeholder="Tối thiểu 6 ký tự")
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    login_btn = st.form_submit_button("Đăng nhập", use_container_width=True)
                with c_btn2:
                    register_btn = st.form_submit_button("Đăng ký mới", use_container_width=True)

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


# ---------------------------------------------------------
# Chat Screen (Protected by Sign-in)
# ---------------------------------------------------------

def render_chat_page():
    user = st.session_state["user"]

    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Tài khoản")
        st.write(f"**Email:** `{user['email']}`")
        st.caption(f"UID: {user['uid']}")

        if st.button("🚪 Đăng xuất", use_container_width=True):
            forget_user()
            st.rerun()

        st.divider()
        st.markdown("### ⚙️ Thông số RAG")
        st.markdown(f"- **Thành phố:** TP. Hồ Chí Minh")
        st.markdown(f"- **Embedding:** `{EMBEDDING_MODEL}`")
        st.markdown(f"- **Chat Model:** `{CHAT_MODEL}`")
        st.markdown(f"- **Top-K:** `{TOP_K}`")
        st.markdown(f"- **Ollama URL:** `{OLLAMA_BASE_URL}`")

        st.divider()
        if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

    # Main Chat Area
    st.title("🏙️ Lumen Travel Assistant - TP.HCM")
    st.caption("Trợ lý tra cứu du lịch chỉ trả lời dựa trên Cẩm nang chính thức (không bịa đặt thông tin).")

    # Load and cache KB embeddings
    try:
        indexed_kb = get_cached_indexed_kb()
    except (RAGError, Exception) as e:
        st.error(f"❌ Không thể khởi tạo cẩm nang RAG: {e}")
        st.info("💡 Vui lòng đảm bảo máy chủ Ollama đang chạy và URL trong file `.env` là chính xác.")
        st.stop()

    # Ensure chat history exists in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display existing chat messages
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("retrieved"):
                with st.expander("📚 Xem các mục cẩm nang được tham khảo & Điểm số (Top-K)"):
                    for entry, score in msg["retrieved"]:
                        st.markdown(
                            f"**[{entry['id']}] {entry['title']}** (Chủ đề: `{entry.get('category', 'Khác')}`) — "
                            f"⭐ Độ tương đồng: `{score:.4f}`\n\n"
                            f"> {entry['text']}\n\n"
                            f"*Nguồn: {entry.get('source', 'Lumen Travel')}*"
                        )
                        st.divider()

    # Chat Input
    user_query = st.chat_input("Hỏi về giờ mở cửa, giá vé, địa điểm tại TP.HCM...")

    if user_query:
        query_text = user_query.strip()
        if not query_text:
            st.warning("Vui lòng nhập câu hỏi.")
            return

        # Show user message immediately
        st.session_state["chat_history"].append({"role": "user", "content": query_text})
        with st.chat_message("user"):
            st.markdown(query_text)

        # Process with RAG
        with st.chat_message("assistant"):
            with st.spinner("Đang tìm kiếm thông tin trong cẩm nang..."):
                try:
                    # 1. Retrieve top-k entries
                    retrieved_results = retrieve_relevant_entries(
                        query=query_text,
                        indexed_kb=indexed_kb,
                        base_url=OLLAMA_BASE_URL,
                        top_k=TOP_K,
                    )

                    # 2. Generate answer
                    answer = generate_rag_answer(
                        query=query_text,
                        retrieved_entries=retrieved_results,
                        base_url=OLLAMA_BASE_URL,
                        chat_model=CHAT_MODEL,
                    )

                    st.markdown(answer)

                    # 3. Show retrieved references
                    if retrieved_results:
                        with st.expander("📚 Xem các mục cẩm nang được tham khảo & Điểm số (Top-K)"):
                            for entry, score in retrieved_results:
                                st.markdown(
                                    f"**[{entry['id']}] {entry['title']}** (Chủ đề: `{entry.get('category', 'Khác')}`) — "
                                    f"⭐ Độ tương đồng: `{score:.4f}`\n\n"
                                    f"> {entry['text']}\n\n"
                                    f"*Nguồn: {entry.get('source', 'Lumen Travel')}*"
                                )
                                st.divider()

                    # Save to session history
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": answer,
                        "retrieved": retrieved_results,
                    })

                except RAGError as err:
                    st.error(f"⚠️ Lỗi RAG: {err}")
                except Exception as ex:
                    st.error(f"⚠️ Đã xảy ra lỗi ngoài ý muốn: {ex}")


# ---------------------------------------------------------
# App Entrypoint
# ---------------------------------------------------------

if "user" not in st.session_state:
    render_auth_page()
else:
    render_chat_page()
