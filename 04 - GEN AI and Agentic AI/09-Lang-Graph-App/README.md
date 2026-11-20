# Simple Banking AI Chatbot

A beginner-friendly project demonstrating a dynamic LangGraph workflow with only four nodes:
1. Router node (LLM classifies the question)
2. DB node (predefined read-only MySQL queries)
3. RAG node (retrieves banking policy chunks from ChromaDB)
4. Response node (LLM formats the answer)

## Prerequisites
- Python 3.10+
- MySQL 8+
- OpenAI API key

## Setup (Windows)
```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

## Database
Open `database/banking.sql` in MySQL Workbench and execute it. It creates the `banking_ai` database and sample tables/records.

## Environment
Copy `.env.example` to `.env` and set your OpenAI key and MySQL credentials.

## Run
```bash
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## RAG ingestion
Put `.txt` or `.pdf` policy files in `policies/`.
In the Streamlit sidebar, click **Ingest policy documents**. This uses OpenAI embeddings and stores vectors locally in `chroma_db`.

## Try these questions
- Show all bank accounts
- How many savings accounts are there?
- Show details for account 1000001001
- Show failed transactions
- Explain the KYC process
- What should an employee do if a debit card is lost?

## Architecture
Question -> LLM Router -> (DB Node OR RAG Node) -> Response Node -> Streamlit

## Important
This is a classroom prototype using fictional data and fictional policy text. It is not production-ready.
Before using real data, add employee authentication, authorization, auditing, account masking, a least-privilege read-only MySQL user, strict query allowlisting, and compliance/security review. Never allow arbitrary LLM-generated SQL to run against a banking database.
