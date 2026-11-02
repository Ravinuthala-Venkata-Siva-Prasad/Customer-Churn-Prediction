
from pathlib import Path

# Project Root Directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Output Directories
ARTIFACT_DIR = ROOT_DIR / "artifacts"
LOG_DIR = ROOT_DIR / "logs"

# Dataset Paths
COMBINED_DATA_PATH = (
    PROCESSED_DATA_DIR / "customer_churn_combined.csv"
)

SPLIT_DATA_PATH = (
    PROCESSED_DATA_DIR / "train_test_split.pkl"
)

# Model Artifacts
MODEL_PATH = ARTIFACT_DIR / "model.pkl"
MODEL_RESULTS_PATH = ARTIFACT_DIR / "model_results.json"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"

# Dataset Configuration
TARGET_COLUMN = "Churn"
ID_COLUMN = "CustomerID"

# Reproducibility
RANDOM_STATE = 42

# Dataset Splitting
TEST_SIZE = 0.20
VALIDATION_SIZE = 0.20

# Model Training
CV_FOLDS = 3
MODEL_SELECTION_METRIC = "f1"

# Create Required Directories
for directory in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ARTIFACT_DIR,
    LOG_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
