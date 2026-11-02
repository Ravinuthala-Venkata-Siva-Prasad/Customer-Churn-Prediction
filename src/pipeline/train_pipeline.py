
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_selection import ModelSelection
from src.components.model_evaluation import ModelEvaluation

from src.config import ARTIFACT_DIR


class TrainingPipeline:

    def run_pipeline(self):

        print("STARTING CUSTOMER CHURN ML PIPELINE")

        # 1. Data ingestion
        ingestion = DataIngestion()

        X_train, X_test, y_train, y_test = (
            ingestion.initiate_data_ingestion()
        )

        # 2. Data validation
        validation = DataValidation()

        validation.initiate_data_validation(
            X_train, X_test, y_train, y_test
        )

        # 3. Data transformation
        transformation = DataTransformation()

        preprocessor = transformation.get_preprocessor(X_train)

        # 4. Train and compare models
        trainer = ModelTrainer()

        trained_models, results_df = (
            trainer.initiate_model_trainer(
                X_train,
                y_train,
                preprocessor
            )
        )

        # 5. Select and save best model
        selection = ModelSelection()

        best_model, best_name = (
            selection.initiate_model_selection(
                trained_models,
                results_df,
                X_train,
                y_train
            )
        )

        # 6. Final model evaluation
        evaluation = ModelEvaluation()

        metrics = evaluation.initiate_model_evaluation(
            best_model,
            X_test,
            y_test
        )

        print("\nBEST MODEL:", best_name)
        print("ARTIFACT DIRECTORY:", ARTIFACT_DIR)
        print("PIPELINE COMPLETED SUCCESSFULLY")

        return metrics


if __name__ == "__main__":

    pipeline = TrainingPipeline()

    pipeline.run_pipeline()
