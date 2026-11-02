
import pandas as pd

from src.config import COMBINED_DATA_PATH


def test_dataset_exists():

    assert COMBINED_DATA_PATH.exists()


def test_dataset_columns():

    df = pd.read_csv(COMBINED_DATA_PATH)

    expected_columns = [
        "CustomerID",
        "Age",
        "Gender",
        "Tenure",
        "Usage Frequency",
        "Support Calls",
        "Payment Delay",
        "Subscription Type",
        "Contract Length",
        "Total Spend",
        "Last Interaction",
        "Churn"
    ]

    assert list(df.columns) == expected_columns


def test_target_values():

    df = pd.read_csv(COMBINED_DATA_PATH)

    assert set(df["Churn"].dropna().unique()).issubset({0, 1})
