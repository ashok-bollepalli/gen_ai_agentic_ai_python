# AI Code Review & Developer Assistant

An educational capstone that reviews Python source code using:
- Python AST syntax/statistics checks
- Ruff linting
- Bandit security scanning
- OpenAI structured LLM review
- LangGraph workflow
- Pytest test-suggestion generation
- Streamlit frontend
- FastAPI REST endpoint

## Requirements
- Python 3.11 or 3.12 recommended
- An OpenAI API key and access to the configured model

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add your API key.

## Run Streamlit UI
```powershell
streamlit run app.py
```
Open the URL shown in the terminal, usually http://localhost:8501.

## Run FastAPI
```powershell
uvicorn api:app --reload
```
Open http://localhost:8000/docs. The `POST /review` request body:
```json
{
  "source_code": "def add(a, b):\\n    return a + b"
}
```

## Run tests
```powershell
pytest -q
```

## How it works
1. Validate and parse source code without executing it.
2. Run Ruff and Bandit on a temporary `.py` file.
3. Ask the LLM for structured findings.
4. Ask the LLM to suggest pytest tests.
5. Return a JSON report and show it in Streamlit.

## Important limitations
- This is an educational MVP, not a security certification tool.
- It currently reviews Python only.
- It does not execute uploaded source code or generated tests.
- AI findings can be wrong or incomplete; require human review.
- Ruff and Bandit findings are signals and must be interpreted in context.
- For multi-user production, add authentication, authorization, per-user storage, rate limits, audit logs, privacy controls, and isolated execution infrastructure.
- The starter API has no authentication and should not be exposed publicly as-is.
- Do not upload confidential source code unless your organization permits sending it to the configured model provider.

## Suggested extensions
1. GitHub pull-request integration with read-only permissions first.
2. Java support using JavaParser or Checkstyle/SpotBugs.
3. RAG over internal coding standards and architecture docs.
4. Human-approved patch generation.
5. CI pipeline that posts review findings but does not auto-merge.
6. Observability for latency, token usage and reviewer quality.
