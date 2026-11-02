
# Customer Churn Prediction – End-to-End Machine Learning Project

An end-to-end Machine Learning application that predicts customer churn using classification models and provides interactive customer analytics through a FastAPI web dashboard.

## Project Overview

Customer churn occurs when customers stop using a company's products or services.

This project uses customer demographic, usage, payment and subscription information to predict whether a customer is likely to leave.

The application includes data preprocessing, exploratory data analysis, model training, evaluation, REST API development, an interactive dashboard, automated testing and Docker containerization.

## Key Features

- Customer data ingestion and validation
- Exploratory Data Analysis (EDA)
- Data preprocessing and feature engineering
- Multiple machine learning model training
- Model selection and evaluation
- Customer churn prediction through REST API
- Interactive analytics dashboard
- Customer churn probability visualization
- Automated testing using Pytest
- Docker containerization

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Matplotlib, Seaborn, Chart.js |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Testing | Pytest, HTTPX |
| Model Storage | Joblib |
| Containerization | Docker |
| Version Control | Git, GitHub |

## Project Structure

Customer-Churn-Prediction/
│
├── app/
│   ├── main.py
│   ├── templates/
│   └── static/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── artifacts/
│
├── notebooks/
│
├── src/
│   ├── components/
│   └── pipeline/
│
├── tests/
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md

## Dataset

The dataset contains customer information such as:

- Age
- Gender
- Tenure
- Usage Frequency
- Support Calls
- Payment Delay
- Subscription Type
- Contract Length
- Total Spend
- Last Interaction

Target variable:

- 0 – Customer retained
- 1 – Customer churned

CustomerID is excluded from model features.

## Machine Learning Workflow

1. Data ingestion
2. Data cleaning and validation
3. Exploratory Data Analysis
4. Data preprocessing
5. Train-test splitting
6. Model training
7. Model selection
8. Model evaluation
9. Model serialization

## Dashboard

The FastAPI application provides:

- Total customer statistics
- Retained and churned customer counts
- Overall churn rate
- Churn distribution chart
- Subscription-based churn analysis
- Contract-based churn analysis
- Customer age distribution
- Individual customer churn prediction

## Installation

Clone the repository:

```bash
git clone https://github.com/Ravinuthala-Venkata-Siva-Prasad/Customer-Churn-Prediction-.git

cd Customer-Churn-Prediction-
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m uvicorn app.main:app --reload
```

Dashboard:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## Automated Testing

Run:

```bash
python -m pytest -v
```

Tests cover:

- Dashboard endpoint
- Model health
- Analytics API
- Prediction API
- Invalid customer inputs

## Docker Deployment

Build the Docker image:

```bash
docker build -t customer-churn-app .
```

Run the container:

```bash
docker run -d --name customer-churn-container -p 8000:8000 customer-churn-app
```

Open:

http://localhost:8000

## Model Artifact

The trained model is stored locally in:

artifacts/model.pkl

The model is excluded from ordinary Git commits because of its large file size.

To run the application, provide the compatible trained model at the expected location.

## Future Improvements

- AWS ECR and ECS deployment
- CI/CD using GitHub Actions
- Model monitoring
- Prediction logging
- Batch customer predictions
- Model explainability

## Author

Ravinuthala Venkata Siva Prasad

GitHub:
https://github.com/Ravinuthala-Venkata-Siva-Prasad

LinkedIn:
https://www.linkedin.com/in/ravinuthala-venkata-siva-prasad/
