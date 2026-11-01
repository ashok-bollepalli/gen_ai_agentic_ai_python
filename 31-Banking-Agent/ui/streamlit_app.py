"""
Streamlit UI - Dashboard + Reports + AI Assistant.
The UI never touches data directly; it ONLY calls the FastAPI backend.

Run:  streamlit run ui/streamlit_app.py
"""
import os
import uuid
from datetime import date

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Bank AI Assistant", page_icon="🏦", layout="wide")


def api_get(path: str, **params):
    params = {k: v for k, v in params.items() if v}
    return requests.get(f"{API_URL}{path}", params=params, timeout=30).json()


def rupees(x: float) -> str:
    return f"₹{x:,.0f}"


# ---------------- Sidebar: date range filter ----------------
st.sidebar.title("🏦 Sample Bank")
start = st.sidebar.date_input("Start date", date(2026, 1, 1))
end = st.sidebar.date_input("End date", date(2026, 10, 31))
s, e = str(start), str(end)

tab_dash, tab_report, tab_chat = st.tabs(["📊 Dashboard", "📄 Reports", "🤖 AI Assistant"])

# ================= TAB 1: DASHBOARD =================
with tab_dash:
    cash = api_get("/analytics/cash-flow", start=s, end=e)
    loans = api_get("/analytics/loans", start=s, end=e)
    acc = api_get("/analytics/accounts")
    revenue = pd.DataFrame(api_get("/analytics/branch-revenue", start=s, end=e))

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Incoming", rupees(cash["incoming"]))
    c2.metric("Outgoing", rupees(cash["outgoing"]))
    c3.metric("Total Revenue", rupees(revenue["total_revenue"].sum()))
    c4.metric("Loan Approval Rate", f"{loans['approval_rate_pct']}%")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Branch Revenue")
        fig = px.bar(revenue, x="branch_name", y=["transaction_fees", "loan_fees"],
                     labels={"value": "Revenue (₹)", "branch_name": "Branch"})
        st.plotly_chart(fig, width="stretch")
    with col2:
        st.subheader("Monthly Incoming vs Outgoing")
        flow = pd.DataFrame(api_get("/analytics/cash-flow/monthly", start=s, end=e))
        fig = px.line(flow, x="month", y=["incoming", "outgoing"], markers=True,
                      labels={"value": "Amount (₹)"})
        st.plotly_chart(fig, width="stretch")

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Loan Status")
        status = pd.DataFrame(loans["by_status"].items(), columns=["status", "count"])
        st.plotly_chart(px.pie(status, names="status", values="count", hole=0.4),
                        width="stretch")
    with col4:
        st.subheader("Loans by Branch")
        lb = pd.DataFrame(api_get("/analytics/loans/by-branch", start=s, end=e))
        cols = [c for c in ["APPROVED", "PENDING", "REJECTED"] if c in lb.columns]
        st.plotly_chart(px.bar(lb, x="branch_name", y=cols, barmode="group"),
                        width="stretch")

    st.caption(f"Accounts: {acc['total_accounts']} | Total balance: {rupees(acc['total_balance'])}"
               f" | Status: {acc['by_status']}")

# ================= TAB 2: REPORTS =================
with tab_report:
    st.subheader(f"Report: {s} → {e}")
    report = api_get("/reports/date-range", start=s, end=e)

    st.write("**Cash Flow**")
    st.dataframe(pd.DataFrame([report["cash_flow"]]), width="stretch")

    st.write("**Branch Revenue**")
    rev_df = pd.DataFrame(report["branch_revenue"])
    st.dataframe(rev_df, width="stretch")

    st.write("**Loans**")
    st.json(report["loans"])

    st.download_button("⬇️ Download revenue report (CSV)", rev_df.to_csv(index=False),
                       file_name=f"branch_revenue_{s}_to_{e}.csv", mime="text/csv")

# ================= TAB 3: AI ASSISTANT =================
with tab_chat:
    st.subheader("Ask anything about bank data or policies")
    st.caption("Try: *Which branch earned most revenue in March 2026?* · "
               "*What credit score is needed for auto loan approval?* · "
               "*How many leaves do I get per year?*")

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.history = []

    for msg in st.session_state.history:
        st.chat_message(msg["role"]).markdown(msg["content"])

    if question := st.chat_input("Type your question..."):
        st.chat_message("user").markdown(question)
        st.session_state.history.append({"role": "user", "content": question})

        with st.spinner("Thinking..."):
            res = requests.post(f"{API_URL}/chat", timeout=120, json={
                "question": question, "session_id": st.session_state.session_id}).json()

        answer = f"{res['answer']}\n\n_🧭 Agent route: `{res.get('route')}`_"
        st.chat_message("assistant").markdown(answer)
        st.session_state.history.append({"role": "assistant", "content": answer})
