"""
Streamlit UI for bank employees.
  Tab 1: Dashboard  -> charts + reports for a date range
  Tab 2: AI Assistant -> chat with BankBuddy (LangGraph agent)

The UI only talks to FastAPI (never to the DB directly).
Run:  streamlit run ui/app.py
"""
import os
import uuid
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="BankBuddy - Employee AI Assistant", page_icon="🏦", layout="wide")
st.title("🏦 BankBuddy — Employee Analytics & AI Assistant")


def api_get(path: str, **params):
    resp = requests.get(f"{API_URL}{path}", params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def rupees(x: float) -> str:
    return f"₹ {x:,.0f}"


# ---------------- Sidebar: date range ----------------
with st.sidebar:
    st.header("📅 Report Date Range")
    start = st.date_input("Start date", date.today() - timedelta(days=180))
    end = st.date_input("End date", date.today())
    st.caption(f"API: {API_URL}")

dates = {"start_date": start.isoformat(), "end_date": end.isoformat()}

dashboard_tab, chat_tab = st.tabs(["📊 Dashboard", "🤖 AI Assistant"])

# ---------------- Dashboard ----------------
with dashboard_tab:
    try:
        revenue = api_get("/api/analytics/revenue", **dates)
        flow = api_get("/api/analytics/cash-flow", **dates)
        loans = api_get("/api/analytics/loans", **dates)
        trend = api_get("/api/analytics/monthly-trend", **dates)
        accounts = api_get("/api/analytics/accounts")
    except Exception as e:
        st.error(f"Could not load data from API: {e}")
        st.stop()

    # KPI cards
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue", rupees(revenue["total_revenue"]))
    c2.metric("Incoming", rupees(flow["total_incoming"]))
    c3.metric("Outgoing", rupees(flow["total_outgoing"]))
    c4.metric("Loan Approval Rate", f'{loans["approval_rate_pct"]}%')
    c5.metric("Total Accounts", accounts["total_accounts"])

    left, right = st.columns(2)

    # Branch revenue
    rev_df = pd.DataFrame(revenue["by_branch"])
    if not rev_df.empty:
        left.plotly_chart(px.bar(rev_df, x="branch_name", y="total_revenue",
                                 title="Revenue by Branch (Fees + Interest)",
                                 labels={"branch_name": "Branch", "total_revenue": "Revenue (₹)"}),
                          width="stretch")

    # Incoming vs outgoing
    flow_df = pd.DataFrame(flow["by_branch"])
    if not flow_df.empty:
        melted = flow_df.melt(id_vars="branch_name", value_vars=["incoming", "outgoing"],
                              var_name="Direction", value_name="Amount")
        right.plotly_chart(px.bar(melted, x="branch_name", y="Amount", color="Direction",
                                  barmode="group", title="Incoming vs Outgoing by Branch",
                                  labels={"branch_name": "Branch", "Amount": "Amount (₹)"}),
                           width="stretch")

    # Monthly trend
    trend_df = pd.DataFrame(trend["months"])
    if not trend_df.empty:
        st.plotly_chart(px.line(trend_df, x="month", y=["incoming", "outgoing", "revenue"],
                                markers=True, title="Monthly Trend",
                                labels={"value": "Amount (₹)", "variable": "Metric"}),
                        width="stretch")

    left2, right2 = st.columns(2)

    # Loans by type
    loan_df = pd.DataFrame(loans["by_type"])
    if not loan_df.empty:
        left2.plotly_chart(px.bar(loan_df, x="loan_type", y=["applications", "approved"],
                                  barmode="group", title="Loan Applications vs Approvals",
                                  labels={"value": "Count", "loan_type": "Loan Type"}),
                           width="stretch")

    # Loan status per branch
    status_df = pd.DataFrame(loans["by_branch_status"])
    if not status_df.empty:
        right2.plotly_chart(px.bar(status_df, x="branch_name", y="loan_count", color="status",
                                   title="Loan Status by Branch",
                                   labels={"branch_name": "Branch", "loan_count": "Loans"}),
                            width="stretch")

    # Report tables + CSV download
    st.subheader("📄 Reports")
    report_choice = st.selectbox("Choose report", ["Branch Revenue", "Cash Flow", "Loans by Type",
                                                   "Accounts by Branch"])
    report_df = {
        "Branch Revenue": rev_df,
        "Cash Flow": flow_df,
        "Loans by Type": loan_df,
        "Accounts by Branch": pd.DataFrame(accounts["by_branch"]),
    }[report_choice]
    st.dataframe(report_df, width="stretch")
    st.download_button("⬇️ Download CSV", report_df.to_csv(index=False),
                       file_name=f"{report_choice.lower().replace(' ', '_')}_{start}_{end}.csv",
                       mime="text/csv")

# ---------------- AI Assistant ----------------
with chat_tab:
    st.caption("Ask about branch revenue, cash flow, loans, accounts — or bank policies (KYC, loans, fees).")

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []

    examples = ["Which branch earned the most revenue last quarter?",
                "Compare incoming and outgoing amounts for Hyderabad this year",
                "What is the loan approval rate by loan type from 2026-01-01 to 2026-06-30?",
                "What documents are needed for KYC?"]
    with st.expander("💡 Example questions"):
        for q in examples:
            st.markdown(f"- {q}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if question := st.chat_input("Ask BankBuddy..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(f"{API_URL}/api/chat", timeout=120,
                                         json={"question": question,
                                               "session_id": st.session_state.session_id})
                    resp.raise_for_status()
                    data = resp.json()
                    answer = data["answer"]
                    if data["tools_used"]:
                        answer += f"\n\n_🔧 Tools used: {', '.join(data['tools_used'])}_"
                except Exception as e:
                    answer = f"⚠️ Error: {e}"
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
