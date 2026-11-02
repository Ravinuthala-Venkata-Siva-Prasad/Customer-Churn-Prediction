
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)


class DataTransformation:

    def get_preprocessor(self, X_train):

        numerical_columns = X_train.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = X_train.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        numerical_pipeline = Pipeline([
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scaler",
                StandardScaler()
            )
        ])

        categorical_pipeline = Pipeline([
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore")
            )
        ])

        preprocessor = ColumnTransformer([
            (
                "numerical",
                numerical_pipeline,
                numerical_columns
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            )
        ])

        print("Numerical columns:", numerical_columns)
        print("Categorical columns:", categorical_columns)

        return preprocessor
