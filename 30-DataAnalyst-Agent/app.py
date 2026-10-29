import os
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

load_dotenv()

st.set_page_config(page_title="Simple AI Data Analyst", page_icon="📊")
st.title("📊 Simple AI Data Analyst Agent")
st.write("Upload a CSV file and ask questions about your data.")

# Step 1: Upload the dataset
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Upload sample_data/sales.csv to try the project.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file)
except Exception:
    st.error("Could not read this CSV file. Please check its format.")
    st.stop()

if df.empty:
    st.error("The CSV file has no rows.")
    st.stop()

st.subheader("1. Preview Your Data")
st.dataframe(df.head(10), use_container_width=True)

st.subheader("2. Ask a Question")
question = st.text_input(
    "What would you like to know?",
    placeholder="Example: Which region has the highest sales?"
)

# Step 2: Define simple tools that the AI can call.
@tool
def show_columns() -> str:
    """Show column names and data types in the uploaded dataset."""
    return json.dumps({
        "columns": {str(c): str(df[c].dtype) for c in df.columns},
        "rows": len(df)
    })

@tool
def calculate_total(column: str) -> str:
    """Calculate the total of a numeric column. Input must be an existing column name."""
    if column not in df.columns:
        return f"Column not found. Available columns: {list(df.columns)}"
    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric."
    return json.dumps({
        "column": column,
        "total": float(df[column].sum())
    })

@tool
def average_value(column: str) -> str:
    """Calculate the average of a numeric column."""
    if column not in df.columns:
        return f"Column not found. Available columns: {list(df.columns)}"
    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric."
    return json.dumps({
        "column": column,
        "average": float(df[column].mean())
    })

@tool
def compare_by_category(category_column: str, value_column: str) -> str:
    """Add a numeric column by category, for example Sales by Region."""
    if category_column not in df.columns or value_column not in df.columns:
        return f"Unknown column. Available columns: {list(df.columns)}"
    if not pd.api.types.is_numeric_dtype(df[value_column]):
        return f"'{value_column}' must be numeric."
    result = (
        df.groupby(category_column, dropna=False)[value_column]
        .sum()
        .sort_values(ascending=False)
    )
    return json.dumps({
        "category_column": category_column,
        "value_column": value_column,
        "results": [
            {"category": str(name), "total": float(value)}
            for name, value in result.items()
        ]
    })

tools = [
    show_columns,
    calculate_total,
    average_value,
    compare_by_category,
]
tool_map = {item.name: item for item in tools}

# Step 3: Ask the model to choose and call the right tool.
if st.button("Analyze", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    if not os.getenv("OPENAI_API_KEY"):
        st.error("Add OPENAI_API_KEY to your .env file and restart Streamlit.")
        st.stop()

    try:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            temperature=0
        ).bind_tools(tools)

        messages = [
            SystemMessage(content=f"""
You are a beginner-friendly data analyst.
Use the available tools to calculate answers from the dataset.
Never guess numerical answers. Use exact column names.
If a question is unclear, ask the user to clarify.
Dataset columns: {list(df.columns)}
"""),
            HumanMessage(content=question)
        ]

        with st.spinner("The AI is analyzing your question..."):
            # One tool-calling round keeps the demo easy to explain.
            response = llm.invoke(messages)
            messages.append(response)

            tool_results = []
            for call in response.tool_calls:
                result = tool_map[call["name"]].invoke(call["args"])
                tool_results.append({
                    "tool": call["name"],
                    "result": result
                })
                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=call["id"]
                    )
                )

            if tool_results:
                final_response = ChatOpenAI(
                    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                    temperature=0
                ).invoke(messages)
                answer = final_response.content
            else:
                answer = response.content

        st.subheader("3. AI Answer")
        st.write(answer)

        if tool_results:
            with st.expander("See which tools the AI called"):
                st.json(tool_results)

            # Show a chart when a category comparison tool was used.
            for item in tool_results:
                if item["tool"] == "compare_by_category":
                    result_data = json.loads(item["result"])
                    chart_df = pd.DataFrame(result_data["results"])
                    if not chart_df.empty:
                        st.subheader("4. Chart")
                        fig, ax = plt.subplots()
                        ax.bar(
                            chart_df["category"],
                            chart_df["total"]
                        )
                        ax.set_xlabel(result_data["category_column"])
                        ax.set_ylabel(result_data["value_column"])
                        ax.set_title(
                            f'{result_data["value_column"]} by '
                            f'{result_data["category_column"]}'
                        )
                        plt.xticks(rotation=30)
                        fig.tight_layout()
                        st.pyplot(fig)
                        plt.close(fig)

    except Exception as exc:
        st.error("Analysis failed. Check your API key, model access, and internet connection.")
        print("Analysis error:", repr(exc))
