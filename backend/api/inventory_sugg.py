from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from database import collection

# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Optimization"]
)

# =====================================================
# Load Model & Encoder
# =====================================================

try:
    inventory_model = joblib.load("models/inventory_model.pkl")
    stock_encoder = joblib.load("models/stockcode_encoder.pkl")

    print("✅ Inventory Model Loaded")

except Exception as e:
    raise RuntimeError(f"Error loading model or encoder: {e}")

# =====================================================
# Request Schema
# =====================================================

class InventoryRequest(BaseModel):
    StockCode: str

# =====================================================
# Inventory Prediction
# =====================================================

@router.post("/predict")
def predict_inventory(request: InventoryRequest):

    try:
        stock_value = int(request.StockCode)
    except ValueError:
        stock_value = request.StockCode.strip()

    

    pipeline = [
        {
            "$match": {
            "StockCode": stock_value
        }
        },
        {
            "$group": {
                "_id": {
                    "StockCode": "$StockCode",
                    "InvoiceDate": "$InvoiceDate"
                },
                "Revenue": {
                    "$sum": "$Revenue"
                },
                "OrderValue": {
                    "$sum": "$OrderValue"
                },
                "BasketSize": {
                    "$avg": "$BasketSize"
                }
            }
        },
        {
            "$sort": {
                "_id.InvoiceDate": 1
            }
        }
    ]

    records = list(collection.aggregate(pipeline))

    if not records:
        raise HTTPException(
            status_code=404,
            detail="StockCode not found."
        )

    stock_df = pd.DataFrame([
        {
            "StockCode": r["_id"]["StockCode"],
            "InvoiceDate": pd.to_datetime(r["_id"]["InvoiceDate"]),
            "Revenue": r["Revenue"],
            "OrderValue": r["OrderValue"],
            "BasketSize": r["BasketSize"]
        }
        for r in records
    ])

    latest = stock_df.iloc[-1]

    try:
        stock_encoded = stock_encoder.transform([request.StockCode])[0]
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Unknown StockCode."
        )

    input_df = pd.DataFrame([{
        "StockCode_Encoded": stock_encoded,
        "Revenue": latest["Revenue"],
        "OrderValue": latest["OrderValue"],
        "BasketSize": latest["BasketSize"]
    }])

    prediction = inventory_model.predict(input_df)[0]

    if hasattr(inventory_model, "predict_proba"):
        probability = inventory_model.predict_proba(input_df)[0][1]
    else:
        probability = float(prediction)

    if probability >= 0.80:
        status = "Critical"
        recommendation = "Reorder inventory immediately."

    elif probability >= 0.50:
        status = "Warning"
        recommendation = "Monitor stock closely."

    else:
        status = "Safe"
        recommendation = "Inventory level is sufficient."

    return {
        "StockCode": request.StockCode,
        "InventoryStatus": status,
        "StockOutRisk": round(probability * 100, 2),
        "Recommendation": recommendation,
        "LastRevenue": round(float(latest["Revenue"]), 2),
        "LastOrderValue": round(float(latest["OrderValue"]), 2),
        "LastBasketSize": round(float(latest["BasketSize"]), 2)
    }