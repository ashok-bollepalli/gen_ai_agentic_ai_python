# Simple AI Data Analyst Agent

A beginner-friendly Gen AI and Agentic AI capstone. Students upload a CSV, ask a natural-language question, and the model chooses from a few safe Pandas tools.

## What students learn
- Read CSV files with Pandas
- Build a Streamlit interface
- Create tools with `@tool`
- Let an LLM select tools using tool calling
- Return calculated results to the LLM for explanation
- Visualize grouped results with Matplotlib
- Use `.env` to configure an API key

## Setup (Windows)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. If the configured model is unavailable, set `OPENAI_MODEL` to a model supported by your account.

## Run
```powershell
streamlit run app.py
```

Upload `sample_data/sales.csv` and try:
- Show me the columns
- Calculate total Sales
- What is the average Profit?
- Compare Sales by Region

## Teaching flow
1. Run the app and preview the CSV.
2. Explain each `@tool` function.
3. Explain `bind_tools(tools)`: it tells the model which tools are available.
4. Explain `response.tool_calls`: the model chooses a tool and supplies arguments.
5. Python executes the tool and returns the result.
6. The model explains the computed result.
7. A chart is drawn using the comparison output.

## Limitations (intentional for beginner version)
- CSV only; no Excel or multi-file support.
- Only four tools and one tool-calling round.
- No database, authentication, RAG, MCP, or deployment setup.
- Tool output/chart behavior is a teaching demo, not a production BI system.
- Uploaded CSV values are data; do not upload sensitive information.
- The app does not execute arbitrary LLM-generated Python.
