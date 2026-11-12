import streamlit as st

from services.data_service import DataService
from tools.data_tools import create_data_tools
from agents.analyst_agent import AnalystAgent
from presentation.charts import display_charts


def render_application():

    st.set_page_config(
        page_title="AI Data Analyst",
        page_icon="📊"
    )

    st.title("📊 Simple AI Data Analyst Agent")

    st.write(
        "Upload a CSV file and ask questions about your data."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info("Please upload a CSV file.")

        return

    try:

        df = DataService.load_csv(uploaded_file)

    except ValueError as exc:

        st.error(str(exc))

        return

    st.subheader("1. Dataset Preview")

    st.dataframe(
        DataService.get_preview(df),
        use_container_width=True
    )

    st.subheader("2. Ask Questions")

    question = st.text_input(
        "What would you like to know?",
        placeholder="Which region has the highest sales?"
    )

    if st.button("Analyze", type="primary"):

        if not question.strip():

            st.warning("Please enter a question.")

            return

        from config.settings import Settings

        if not Settings.OPENAI_API_KEY:

            st.error("OPENAI_API_KEY is missing.")

            return

        try:

            with st.spinner("Analyzing dataset..."):

                tools = create_data_tools(df)

                agent = AnalystAgent(tools)

                result = agent.analyze(
                    question,
                    DataService.get_columns(df)
                )

            st.subheader("3. AI Answer")

            st.write(result["answer"])

            if result["tool_results"]:

                with st.expander("View Tool Execution"):

                    st.json(result["tool_results"])

                display_charts(
                    result["tool_results"]
                )

        except Exception as exc:

            st.error(
                "Analysis failed. Please check your API key and model."
            )

            print("Analysis error:", repr(exc))