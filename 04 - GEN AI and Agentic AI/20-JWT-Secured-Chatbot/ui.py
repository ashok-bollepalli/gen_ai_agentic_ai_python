"""
ui.py - Streamlit UI. Login/Register when logged out, chat when logged in.
Run: streamlit run ui.py
"""
import requests
import streamlit as st

from config import config

st.set_page_config(page_title="Gen AI Chatbot", page_icon="🤖")
st.title("🤖 Gen AI Chatbot")
st.session_state.setdefault("token", None)
st.session_state.setdefault("username", None)
st.session_state.setdefault("messages", [])


def post(path, payload, token=None):
    """POST to the backend (adds JWT header if token given). Returns (status, json)."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        res = requests.post(config.BACKEND_URL + path, json=payload, headers=headers, timeout=60)
        return res.status_code, res.json()
    except requests.exceptions.ConnectionError:
        return 0, {"detail": "Backend is not running. Start it with: python backend_service.py"}


def logout():
    st.session_state.update(token=None, username=None, messages=[])


def auth_page():
    if notice := st.session_state.pop("notice", None):
        st.warning(notice)

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab, st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            status, data = post("/login", {"username": username, "password": password})
            if status == 200:
                st.session_state.update(token=data["access_token"], username=data["username"])
                st.rerun()
            else:
                st.error(data.get("detail", "Login failed"))

    with register_tab, st.form("register"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            status, data = post("/register", {"username": username, "email": email, "password": password})
            if status == 200:
                st.success("Registered! Please login now.")
            else:
                st.error(data.get("detail", "Registration failed"))


def chat_page():
    st.sidebar.write(f"Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.chat_message("user").markdown(prompt)
        with st.spinner("Thinking..."):
            status, data = post("/chat", {"message": prompt, "history": st.session_state.messages},
                                st.session_state.token)

        if status == 200:
            st.session_state.messages += [{"role": "user", "content": prompt},
                                          {"role": "assistant", "content": data["reply"]}]
            st.chat_message("assistant").markdown(data["reply"])
        elif status == 401:
            logout()
            st.session_state.notice = "Session expired. Please login again."
            st.rerun()
        else:
            st.error(data.get("detail", "Something went wrong"))


if st.session_state.token:
    chat_page()
else:
    auth_page()