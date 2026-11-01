# 🏦 Bank Agentic AI — Capstone Project

An **employee-friendly AI assistant + analytics dashboard** for a bank.
Employees can see branch revenue, incoming/outgoing money, loan approvals and date-range
reports — and simply *ask questions in plain English* about data or bank policies.

**Tech stack:** Python · MySQL · SQLAlchemy · Pandas · Plotly · OpenAI · LangChain · RAG + Chroma DB · LangGraph · MCP · FastAPI · Streamlit

---

## 1. Architecture

```mermaid
flowchart LR
    U[👩‍💼 Bank Employee] --> UI[Streamlit UI<br/>Dashboard · Reports · Chat]
    UI -->|REST| API[FastAPI]
    API -->|/analytics/*| AN[Analytics Service<br/>Pandas]
    API -->|/chat| AG[LangGraph Agent]

    AG --> R{Router<br/>LLM}
    R -->|analytics| AL[Analyst Node]
    R -->|policy| RAG[Policy RAG Node]
    R -->|general| GN[General Node]

    AL <-->|tool calls| T[LangChain Tools]
    T --> AN
    RAG --> VDB[(Chroma Vector DB<br/>policy docs)]

    MCP[MCP Server] --> AN
    MCP --> VDB
    EXT[Claude Desktop / Cursor /<br/>MCP client demo] --> MCP

    AN --> DB[(MySQL bank_db<br/>branches · accounts · transactions · loans)]
```

**Golden rule of this project:** business logic lives in ONE place (`app/services/analytics.py`).
FastAPI, LangChain tools and the MCP server are all just *thin wrappers* over it.

```
Layer            File                              Job
──────────────── ───────────────────────────────── ─────────────────────────────────
Database         data/schema.sql, seed_mysql.py    MySQL tables + sample data
DB access        app/db.py                         SQLAlchemy engine, run_query()
Analytics        app/services/analytics.py         SQL fetch + Pandas calculations
RAG              app/rag/vector_store.py           Policy docs → chunks → Chroma
Tools            app/agent/tools.py                LangChain @tool wrappers
Agent            app/agent/graph.py                LangGraph: router + nodes + memory
MCP              mcp_server/server.py              Same tools exposed via MCP
API              app/api/main.py                   FastAPI endpoints
UI               ui/streamlit_app.py               Dashboard + Reports + Chat
```

## 2. Folder structure

```
banking-agentic-ai/
├── data/
│   ├── schema.sql              # MySQL tables, keys, indexes
│   ├── generate_data.py        # sample data (DataFrames)
│   ├── seed_mysql.py           # creates tables + inserts data
│   └── policies/               # documents for RAG (loan, account, fees, HR)
├── app/
│   ├── config.py               # settings from .env
│   ├── db.py                   # MySQL connection
│   ├── services/analytics.py   # 📊 data analysis
│   ├── rag/vector_store.py     # 📚 RAG + Chroma
│   ├── agent/tools.py          # 🔧 LangChain tools
│   ├── agent/graph.py          # 🧠 LangGraph agent
│   └── api/main.py             # 🌐 FastAPI
├── mcp_server/
│   ├── server.py               # 🔌 MCP server
│   └── client_demo.py          # agent using tools FROM MCP
├── ui/streamlit_app.py         # 🖥️ Streamlit UI
├── docker-compose.yml          # MySQL 8 in one command
├── requirements.txt
└── .env.example
```

## 3. Setup & Run (6 steps)

```bash
# 1. Create virtual env and install
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Add your OpenAI key and MySQL URL
cp .env.example .env               # then edit OPENAI_API_KEY (and DATABASE_URL if needed)

# 3. Start MySQL (Docker) — or use your own MySQL 8 server
docker compose up -d

# 4. Create tables + load sample data, then build the vector DB
python -m data.seed_mysql
python -m app.rag.vector_store

# 5. Start backend  (terminal 1)  → http://localhost:8000/docs
uvicorn app.api.main:app --reload

# 6. Start UI       (terminal 2)  → http://localhost:8501
streamlit run ui/streamlit_app.py
```

**MCP demo (optional):**
```bash
python -m mcp_server.client_demo     # LangGraph agent using tools loaded from MCP server
```

To use the MCP server in **Claude Desktop**, add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "bank-analytics": {
      "command": "/full/path/to/.venv/bin/python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/full/path/to/banking-agentic-ai"
    }
  }
}
```

### Using your own MySQL (no Docker)

```sql
CREATE DATABASE bank_db;
CREATE USER 'bank_user'@'localhost' IDENTIFIED BY 'bank_pass';
GRANT ALL ON bank_db.* TO 'bank_user'@'localhost';
```
Then set `DATABASE_URL=mysql+pymysql://bank_user:bank_pass@localhost:3306/bank_db` in `.env`.

## 4. Features

| Feature | Where |
|---|---|
| Accounts analysis (status, type, balance) | `/analytics/accounts`, Dashboard |
| Branch total revenue (txn fees + loan fees) | `/analytics/branch-revenue`, bar chart |
| Incoming vs outgoing (monthly trend) | `/analytics/cash-flow/monthly`, line chart |
| Loan approvals (status, rate, by branch) | `/analytics/loans`, pie + grouped bar |
| Date-range report + CSV download | `/reports/date-range`, Reports tab |
| AI Assistant (data + policy Q&A, chat memory) | `/chat`, AI Assistant tab |
| MCP tools for any MCP client | `mcp_server/server.py` |

## 5. Sample questions for the AI Assistant

| Question | Agent route |
|---|---|
| Which branch earned the highest revenue in March 2026? | analytics → `get_branch_revenue` |
| Compare incoming and outgoing for BR001 in April 2026 | analytics → `get_incoming_outgoing` |
| What is the loan approval rate this year? | analytics → `get_loan_summary` |
| Show details of account AC1005 | analytics → `get_account_details` |
| Give me a report from 2026-06-01 to 2026-06-30 | analytics → `get_date_range_report` |
| What credit score is needed for automatic approval? | policy (RAG) |
| How do I reactivate a dormant account? | policy (RAG) |
| How many casual leaves do I get? | policy (RAG) |
| Hi! What can you do? | general |

## 6. Business rules used in sample data

- **Revenue** = 0.5% fee on every transaction + 1% processing fee on approved loans
- **Loan status**: credit score ≥ 700 → APPROVED, 650–699 → PENDING, < 650 → REJECTED
- **Incoming** = CREDIT transactions, **Outgoing** = DEBIT transactions

## 7. Suggested teaching order (one module per session)

1. **Data + Pandas** — `generate_data.py`, `analytics.py` (run functions in a notebook)
2. **FastAPI** — `api/main.py`, explore `/docs`
3. **Streamlit + Plotly** — dashboard and reports tabs
4. **RAG** — load → split → embed → store → retrieve in `vector_store.py`
5. **LangChain tools** — `@tool` + why docstrings matter
6. **LangGraph** — state, nodes, conditional edges, tool loop, memory (`graph.py`)
7. **MCP** — same tools as a server; `client_demo.py` plugs them into the agent
8. **End-to-end demo** — ask questions in the UI and show the route used

## 8. Student extension ideas

- Move the grouping into SQL (`GROUP BY`) and compare speed with Pandas
- Add a text-to-SQL tool so the agent can answer new questions with safe read-only queries
- Add a guardrail node that masks account numbers before answering
- Add a "draft email to branch manager" tool
- Add role-based access (teller vs manager) in FastAPI
- Add Slack integration to ask the assistant from Slack
- Add evaluation: a list of test questions with expected tool calls
