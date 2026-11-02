"""
FastAPI backend.
  /api/analytics/*  -> REST endpoints for the Streamlit dashboard (charts)
  /api/chat         -> AI assistant (LangGraph agent)
  /health           -> Kubernetes probes

Run:  uvicorn app.api.main:app --port 8000 --reload
"""
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.agent.graph import BankAgent
from app.services import analytics_service as svc

app = FastAPI(title="Banking Agentic AI API", version="1.0")
agent = BankAgent()


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    tools_used: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- Analytics (dashboard) ----------------
# Optional date filters (YYYY-MM-DD). Empty -> last 90 days.
Start = Annotated[str | None, Query(description="YYYY-MM-DD")]
End = Annotated[str | None, Query(description="YYYY-MM-DD")]


def _safe(fn, *args):
    try:
        return fn(*args)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/analytics/branches")
def branches():
    return svc.list_branches()


@app.get("/api/analytics/accounts")
def accounts():
    return svc.accounts_summary()


@app.get("/api/analytics/revenue")
def revenue(start_date: Start = None, end_date: End = None):
    return _safe(svc.branch_revenue, start_date, end_date)


@app.get("/api/analytics/cash-flow")
def cash_flow(start_date: Start = None, end_date: End = None):
    return _safe(svc.cash_flow, start_date, end_date)


@app.get("/api/analytics/monthly-trend")
def monthly_trend(start_date: Start = None, end_date: End = None):
    return _safe(svc.monthly_trend, start_date, end_date)


@app.get("/api/analytics/loans")
def loans(start_date: Start = None, end_date: End = None):
    return _safe(svc.loan_approvals, start_date, end_date)


@app.get("/api/analytics/top-accounts")
def top_accounts(limit: int = 10):
    return svc.top_accounts(limit)


@app.get("/api/analytics/report")
def report(start_date: Start = None, end_date: End = None):
    return _safe(svc.full_report, start_date, end_date)


# ---------------- AI Assistant ----------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")
    try:
        return await agent.chat(req.question, req.session_id)
    except Exception as e:  # keep the demo friendly
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")
