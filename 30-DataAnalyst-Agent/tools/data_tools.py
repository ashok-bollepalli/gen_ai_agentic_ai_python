import json
import pandas as pd

from langchain_core.tools import tool


def create_data_tools(df):

    @tool
    def show_columns() -> str:
        """Show dataset columns, data types and row count."""

        return json.dumps({
            "columns": {
                str(c): str(df[c].dtype)
                for c in df.columns
            },
            "rows": len(df)
        })

    @tool
    def calculate_total(column: str) -> str:
        """Calculate total of a numeric column."""

        if column not in df.columns:
            return f"Column not found: {column}"

        if not pd.api.types.is_numeric_dtype(df[column]):
            return f"{column} is not numeric"

        return json.dumps({
            "column": column,
            "total": float(df[column].sum())
        })

    @tool
    def average_value(column: str) -> str:
        """Calculate average of a numeric column."""

        if column not in df.columns:
            return f"Column not found: {column}"

        if not pd.api.types.is_numeric_dtype(df[column]):
            return f"{column} is not numeric"

        return json.dumps({
            "column": column,
            "average": float(df[column].mean())
        })

    @tool
    def compare_by_category(
        category_column: str,
        value_column: str
    ) -> str:
        """Calculate sum of a numeric column grouped by category."""

        if category_column not in df.columns:
            return f"Unknown category column: {category_column}"

        if value_column not in df.columns:
            return f"Unknown value column: {value_column}"

        if not pd.api.types.is_numeric_dtype(df[value_column]):
            return f"{value_column} must be numeric"

        result = (
            df.groupby(category_column, dropna=False)[value_column]
            .sum()
            .sort_values(ascending=False)
        )

        return json.dumps({
            "category_column": category_column,
            "value_column": value_column,
            "results": [
                {
                    "category": str(name),
                    "total": float(value)
                }
                for name, value in result.items()
            ]
        })

    return [
        show_columns,
        calculate_total,
        average_value,
        compare_by_category
    ]