from pathlib import Path

ROOT_DIR = Path(r"D:\Customer Churn Prediction").resolve().parent.parent

data_dir = ROOT_DIR/"data"
raw_data_dir = data_dir/"raw"
processed_data_dir = data_dir/"processed"

artifact_dir = ROOT_DIR/"artifacts"
log_dir = ROOT_DIR/"logs"

combined_data_path = processed_data_dir/"customer_churn_combined.csv"
split_data_path = processed_data_dir/"train_test_split.plk"

model_path = artifact_dir/"model.pkl"
model_result_path = artifact_dir/"model_results.json"
metrics_path = artifact_dir/"metrics.json"

target_column = 'Churn'
id_column = 'CustomerID'

random_state = 42
test_size = 0.20
validation_size = 0.20

cv_folds = 3
model_selection_metric = "f1"