
import pandas as pd


class DataValidation:

    def initiate_data_validation(
        self, X_train, X_test, y_train, y_test
    ):

        if X_train.empty or X_test.empty:
            raise ValueError("Training or testing data is empty")

        if len(X_train) != len(y_train):
            raise ValueError("Training feature and target sizes differ")

        if len(X_test) != len(y_test):
            raise ValueError("Testing feature and target sizes differ")

        if list(X_train.columns) != list(X_test.columns):
            raise ValueError("Training and testing columns differ")

        if not set(pd.Series(y_train).dropna().unique()).issubset({0, 1}):
            raise ValueError("Invalid training target values")

        if not set(pd.Series(y_test).dropna().unique()).issubset({0, 1}):
            raise ValueError("Invalid testing target values")

        if pd.Series(y_train).isna().any():
            raise ValueError("Missing labels in training data")

        if pd.Series(y_test).isna().any():
            raise ValueError("Missing labels in testing data")

        print("Data validation successful")

        return True
