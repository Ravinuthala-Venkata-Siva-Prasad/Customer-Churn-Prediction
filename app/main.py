
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "artifacts" / "model.pkl"

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer_churn_combined.csv"
)

TEMPLATE_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"


app = FastAPI(
    title="Customer Churn Prediction",
    description="Customer Churn Prediction and Analytics Dashboard",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

model = None


@app.on_event("startup")
def load_model():

    global model

    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Trained model not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    print("ML model loaded successfully.")

class CustomerData(BaseModel):

    Age: int = Field(ge=18, le=120)

    Gender: str

    Tenure: int = Field(ge=0)

    Usage_Frequency: int = Field(ge=0)

    Support_Calls: int = Field(ge=0)

    Payment_Delay: int = Field(ge=0)

    Subscription_Type: str

    Contract_Length: str

    Total_Spend: float = Field(ge=0)

    Last_Interaction: int = Field(ge=0)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.get("/analytics")
def analytics():

    if not DATA_PATH.exists():

        raise HTTPException(
            status_code=404,
            detail="Combined customer dataset not found."
        )

    try:

        df = pd.read_csv(DATA_PATH)

        required_columns = [
            "Age",
            "Subscription Type",
            "Contract Length",
            "Churn"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:

            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {missing_columns}"
            )

        df = df.dropna(subset=["Churn"])

        df["Churn"] = pd.to_numeric(
            df["Churn"],
            errors="coerce"
        )

        df = df.dropna(subset=["Churn"])

        df = df[df["Churn"].isin([0, 1])]

        if df.empty:

            raise HTTPException(
                status_code=400,
                detail="No valid customer records found."
            )

        # Overall customer counts

        churn_counts = (
            df["Churn"]
            .value_counts()
            .reindex([0, 1], fill_value=0)
        )

        total_customers = len(df)

        retained_customers = int(churn_counts[0])

        churned_customers = int(churn_counts[1])

        churn_rate = (
            churned_customers / total_customers
        ) * 100

        # Churn by subscription

        subscription_churn = (
            df.groupby("Subscription Type", observed=False)["Churn"]
            .mean()
            .mul(100)
            .round(2)
            .to_dict()
        )

        # Churn by contract

        contract_churn = (
            df.groupby("Contract Length", observed=False)["Churn"]
            .mean()
            .mul(100)
            .round(2)
            .to_dict()
        )

        # Customer age distribution

        age_values = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

        age_bins = [
            17, 25, 35, 45, 55, 65, float("inf")
        ]

        age_labels = [
            "18-25",
            "26-35",
            "36-45",
            "46-55",
            "56-65",
            "65+"
        ]

        age_groups = pd.cut(
            age_values,
            bins=age_bins,
            labels=age_labels,
            include_lowest=True
        )

        age_distribution = (
            age_groups
            .value_counts()
            .reindex(age_labels, fill_value=0)
            .to_dict()
        )

        return {

            "total_customers": int(total_customers),

            "retained_customers": retained_customers,

            "churned_customers": churned_customers,

            "churn_rate": round(float(churn_rate), 2),

            "churn_distribution": {
                "Retained": retained_customers,
                "Churned": churned_customers
            },

            "subscription_churn": {
                str(key): float(value)
                for key, value in subscription_churn.items()
            },

            "contract_churn": {
                str(key): float(value)
                for key, value in contract_churn.items()
            },

            "age_distribution": {
                str(key): int(value)
                for key, value in age_distribution.items()
            }

        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Analytics error: {str(error)}"
        )

@app.post("/predict")
def predict_churn(customer: CustomerData):

    if model is None:

        raise HTTPException(
            status_code=503,
            detail="ML model is not loaded."
        )

    try:

        input_data = pd.DataFrame([{

            "Age": customer.Age,

            "Gender": customer.Gender,

            "Tenure": customer.Tenure,

            "Usage Frequency": customer.Usage_Frequency,

            "Support Calls": customer.Support_Calls,

            "Payment Delay": customer.Payment_Delay,

            "Subscription Type": customer.Subscription_Type,

            "Contract Length": customer.Contract_Length,

            "Total Spend": customer.Total_Spend,

            "Last Interaction": customer.Last_Interaction

        }])

        expected_features = getattr(
            model,
            "feature_names_in_",
            input_data.columns.tolist()
        )

        input_data = input_data[list(expected_features)]

        prediction = int(model.predict(input_data)[0])

        probability = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(input_data)[0]

            classes = list(model.classes_)

            if 1 in classes:

                probability = float(
                    probabilities[classes.index(1)]
                )

        result = (
            "Customer Likely to Churn"
            if prediction == 1
            else "Customer Likely to Stay"
        )

        risk = (
            "High"
            if prediction == 1
            else "Low"
        )

        if probability is not None:

            risk = (
                "High"
                if probability >= 0.5
                else "Low"
            )

        return {

            "prediction": prediction,

            "result": result,

            "risk": risk,

            "churn_probability": (
                round(probability * 100, 2)
                if probability is not None
                else None
            )

        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {str(error)}"
        )
