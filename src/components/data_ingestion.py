
import pandas as pd

from src.config import COMBINED_DATA_PATH, SPLIT_DATA_PATH
from src.utils import load_object


class DataIngestion:

    def initiate_data_ingestion(self):

        if not COMBINED_DATA_PATH.exists():
            raise FileNotFoundError(
                f"Dataset not found: {COMBINED_DATA_PATH}"
            )

        df = pd.read_csv(COMBINED_DATA_PATH)
        print("Dataset loaded:", df.shape)

        if not SPLIT_DATA_PATH.exists():
            raise FileNotFoundError(
                f"Train-test split not found: {SPLIT_DATA_PATH}. "
                "Save it from the EDA notebook first."
            )

        X_train, X_test, y_train, y_test = load_object(
            SPLIT_DATA_PATH
        )

        print("Training features:", X_train.shape)
        print("Testing features:", X_test.shape)

        return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.initiate_data_ingestion()
