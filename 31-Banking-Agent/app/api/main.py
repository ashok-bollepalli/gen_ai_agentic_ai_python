"""
FastAPI backend - REST APIs for the dashboard + the AI assistant.

Run:   uvicorn app.api.main:app --reload
Docs:  http://localhost:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel

from app.services import analytics
from app.agent.graph import ask
from app.rag.vector_store import build_index

app = FastAPI(title="Bank Agentic AI API", version="1.0")


# ---------- Request / Response models ----------
class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    route: str | None = None


# ---------- Health ----------
@app.get("/")
def health():
    return {"status": "ok", "docs": "/docs"}


# ---------- Analytics APIs (no AI, pure Pandas) ----------
@app.get("/analytics/accounts")
def accounts():
    return analytics.accounts_summary()


@app.get("/analytics/accounts/{account_id}")
def account(account_id: str):
    return analytics.account_details(account_id)


@app.get("/analytics/cash-flow")
def cash_flow(start: str | None = None, end: str | None = None, branch_id: str | None = None):
    return analytics.incoming_outgoing(start, end, branch_id)


@app.get("/analytics/cash-flow/monthly")
def cash_flow_monthly(start: str | None = None, end: str | None = None):
    return analytics.monthly_cash_flow(start, end)


@app.get("/analytics/branch-revenue")
def revenue(start: str | None = None, end: str | None = None):
    return analytics.branch_revenue(start, end)


@app.get("/analytics/loans")
def loans(start: str | None = None, end: str | None = None):
    return analytics.loan_summary(start, end)


@app.get("/analytics/loans/by-branch")
def loans_branch(start: str | None = None, end: str | None = None):
    return analytics.loans_by_branch(start, end)


@app.get("/reports/date-range")
def report(start: str, end: str):
    return analytics.date_range_report(start, end)


# ---------- AI Assistant ----------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ask(req.question, req.session_id)


@app.post("/rag/rebuild")
def rebuild_index():
    return {"chunks_indexed": build_index()}
