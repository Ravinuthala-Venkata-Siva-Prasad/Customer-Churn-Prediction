
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from src.config import METRICS_PATH
from src.utils import save_json


class ModelEvaluation:

    def initiate_model_evaluation(
        self,
        model,
        X_test,
        y_test
    ):

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": float(
                accuracy_score(y_test, predictions)
            ),

            "precision": float(
                precision_score(
                    y_test, predictions, zero_division=0
                )
            ),

            "recall": float(
                recall_score(
                    y_test, predictions, zero_division=0
                )
            ),

            "f1_score": float(
                f1_score(
                    y_test, predictions, zero_division=0
                )
            ),

            "roc_auc": float(
                roc_auc_score(y_test, probabilities)
            )
        }

        print("\nFINAL TEST RESULTS")
        print(metrics)

        print("\nClassification Report")
        print(classification_report(y_test, predictions))

        print("\nConfusion Matrix")
        print(confusion_matrix(y_test, predictions))

        save_json(str(METRICS_PATH), metrics)

        return metrics
