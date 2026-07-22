from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np

# Import RFM function
from api.customer_seg import calculate_rfm

router = APIRouter(
    prefix="/churn",
    tags=["Customer Churn Prediction"]
)

# ===========================================
# Load Model
# ===========================================

model = joblib.load("models/best_churn_model.pkl")

# ===========================================
# Request Schema
# ===========================================

class CustomerRequest(BaseModel):
    customer_id: int

# ===========================================
# Churn Prediction API
# ===========================================

@router.post("/predict-cust_ID")
def predict_churn(request: CustomerRequest):

    # Calculate RFM
    rfm = calculate_rfm(request.customer_id)

    # Convert to DataFrame
    input_data = pd.DataFrame([{
        "Recency": rfm["Recency"],
        "Frequency": rfm["Frequency"],
        "Monetary": rfm["Monetary"]
    }])


    # Prediction
    prediction = int(model.predict(input_data)[0])

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    # Risk Level
    if probability >= 0.80:
        risk = "Very High"

    elif probability >= 0.60:
        risk = "High"

    elif probability >= 0.40:
        risk = "Medium"

    else:
        risk = "Low"

    return {

        "CustomerID": request.customer_id,

        "Prediction": "Churn"
        if prediction == 1
        else "Not Churn",

        "ChurnProbability": round(probability,4),

        "RiskLevel": risk
    }

class CustomerRequest1(BaseModel):
    Recency : int
    Frequency : int
    Monetary : float


@router.post("/predict-rfm")
def predict_churn(request:CustomerRequest1):
    input_data = np.array([[
        request.Recency,
        request.Frequency,
        request.Monetary
    ]])
    prediction = int(model.predict(input_data)[0])
    pred_prob = float(model.predict_proba(input_data)[0][1])
    return {
        "prediction" : "Churn"if prediction==1 else "No Churn",
        "Probility" :  round(pred_prob,4)
    }