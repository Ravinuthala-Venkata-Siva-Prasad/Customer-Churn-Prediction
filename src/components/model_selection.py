
from src.config import MODEL_PATH,MODEL_RESULTS_PATH,MODEL_SELECTION_METRIC
from src.utils import save_object, save_json


class ModelSelection:

    def initiate_model_selection(
        self,
        trained_models,
        results_df,
        X_train,
        y_train
    ):

        best_result = results_df.sort_values(
            by=MODEL_SELECTION_METRIC,
            ascending=False
        ).iloc[0]

        best_name = best_result["model"]

        print("\nBest model:", best_name)

        best_model = trained_models[best_name]

        # Refit the selected pipeline on all training data.
        best_model.fit(X_train, y_train)

        save_object(str(MODEL_PATH), best_model)

        results = results_df.to_dict(orient="records")

        save_json(
            str(MODEL_RESULTS_PATH),
            results
        )

        print("Best model saved:", MODEL_PATH)

        return best_model, best_name
