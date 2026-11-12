import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def display_charts(tool_results):

    for item in tool_results:

        if item["tool"] == "compare_by_category":

            result_data = json.loads(item["result"])

            chart_df = pd.DataFrame(
                result_data["results"]
            )

            if chart_df.empty:
                continue

            st.subheader("📊 Data Visualization")

            fig, ax = plt.subplots()

            ax.bar(
                chart_df["category"],
                chart_df["total"]
            )

            ax.set_xlabel(
                result_data["category_column"]
            )

            ax.set_ylabel(
                result_data["value_column"]
            )

            ax.set_title(
                f'{result_data["value_column"]} by '
                f'{result_data["category_column"]}'
            )

            plt.xticks(rotation=30)

            fig.tight_layout()

            st.pyplot(fig)

            plt.close(fig)