import pandas as pd


class DataService:

    @staticmethod
    def load_csv(uploaded_file):

        try:
            df = pd.read_csv(uploaded_file)

            if df.empty:
                raise ValueError("CSV file is empty")

            if len(df.columns) == 0:
                raise ValueError("No columns found")

            return df

        except Exception as exc:
            raise ValueError(
                f"Unable to read CSV: {exc}"
            )

    @staticmethod
    def get_preview(df, rows=10):

        return df.head(rows)

    @staticmethod
    def get_columns(df):

        return list(df.columns)