import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score

from xgboost import XGBClassifier
from src.config import RANDOM_STATE,VALIDATION_SIZE

class ModelTrainer:

    def initiate_model_trainer(
        self, X_train, y_train, preprocessor
    ):

        X_fit, X_val, y_fit, y_val = train_test_split(
            X_train,
            y_train,
            test_size=VALIDATION_SIZE,
            random_state=RANDOM_STATE,
            stratify=y_train
        )

        models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            ),

            "Decision Tree": DecisionTreeClassifier(
                max_depth=15,
                class_weight="balanced",
                random_state=RANDOM_STATE
            ),

            "Random Forest": RandomForestClassifier(
                n_estimators=150,
                max_depth=20,
                class_weight="balanced",
                n_jobs=-1,
                random_state=RANDOM_STATE
            ),

            "KNN": KNeighborsClassifier(
                n_neighbors=5,
                weights="distance",
                n_jobs=-1
            ),

            "XGBoost": XGBClassifier(
                n_estimators=150,
                max_depth=6,
                learning_rate=0.1,
                eval_metric="logloss",
                random_state=RANDOM_STATE,
                n_jobs=-1
            ),

            "Gradient Boosting": GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                random_state=RANDOM_STATE
            )
        }

        trained_models = {}
        results = []

        for name, classifier in models.items():

            print(f"\nTraining {name}...")

            pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("classifier", classifier)
            ])

            pipeline.fit(X_fit, y_fit)

            predictions = pipeline.predict(X_val)

            probabilities = pipeline.predict_proba(X_val)[:, 1]

            metrics = {
                "model": name,
                "accuracy": float(
                    accuracy_score(y_val, predictions)
                ),
                "precision": float(
                    precision_score(
                        y_val, predictions, zero_division=0
                    )
                ),
                "recall": float(
                    recall_score(
                        y_val, predictions, zero_division=0
                    )
                ),
                "f1": float(
                    f1_score(
                        y_val, predictions, zero_division=0
                    )
                ),
                "roc_auc": float(
                    roc_auc_score(y_val, probabilities)
                )
            }

            results.append(metrics)
            trained_models[name] = pipeline

            print(metrics)

        results_df = pd.DataFrame(results)

        results_df = results_df.sort_values(
            by="f1",
            ascending=False
        )

        print("\nMODEL COMPARISON")
        print(results_df.to_string(index=False))

        return trained_models, results_df
