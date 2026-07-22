from fastapi import APIRouter, Query
import joblib

router = APIRouter(
    prefix="/forecast",
    tags=["Demand Forecasting"]
)

# Load Prophet Model
model = joblib.load("models/prophate_forecast_model.pkl")


@router.get("/predict")
def predict_forecast(days: int = Query(default=30, ge=1, le=365)):

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    result = forecast.tail(days)[["ds", "yhat"]].copy()
    result.columns = ["Date", "ForecastRevenue"]

    return {
        "ForecastPeriod": f"Next {days} Days",
        "TotalForecastRevenue": round(result["ForecastRevenue"].sum(), 2),
        "AverageDailyRevenue": round(result["ForecastRevenue"].mean(), 2),
        "HighestForecastRevenue": round(result["ForecastRevenue"].max(), 2),
        "LowestForecastRevenue": round(result["ForecastRevenue"].min(), 2),
        "DailyForecast": result.to_dict(orient="records")
    }



import joblib
import pandas as pd
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel
from database import collection

product_model = joblib.load("models/product_demand_model.pkl")
stock_encoder = joblib.load("models/stockcode_encoder.pkl")
day_encoder = joblib.load("models/dayofweek_encoder.pkl")


class ForecastRequest(BaseModel):
    StockCode: str


@router.post("/product")
def predict_product(request: ForecastRequest):

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
                "Quantity": {
                    "$sum": "$Quantity"
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
            "Quantity": r["Quantity"],
            "Revenue": r["Revenue"],
            "OrderValue": r["OrderValue"],
            "BasketSize": r["BasketSize"]
        }
        for r in records
    ])

    if len(stock_df) < 4:
        raise HTTPException(
            status_code=400,
            detail="Not enough historical data."
        )

    latest = stock_df.iloc[-1]

    lag1 = stock_df.iloc[-1]["Quantity"]
    lag2 = stock_df.iloc[-2]["Quantity"]
    lag3 = stock_df.iloc[-3]["Quantity"]

    today = datetime.today()
    day_name = today.strftime("%A")

    stock_encoded = stock_encoder.transform([request.StockCode])[0]
    day_encoded = day_encoder.transform([day_name])[0]

    input_df = pd.DataFrame([{
        "StockCodeEncoded": stock_encoded,
        "Revenue": latest["Revenue"],
        "OrderValue": latest["OrderValue"],
        "BasketSize": latest["BasketSize"],
        "Year": today.year,
        "Month": today.month,
        "Day": today.day,
        "DayOfWeek": day_encoded,
        "IsWeekend": 1 if today.weekday() >= 5 else 0,
        "Lag1": lag1,
        "Lag2": lag2,
        "Lag3": lag3
    }])

    prediction = product_model.predict(input_df)[0]

    forecast_demand = max(0, round(prediction))

    current_stock = 120
    safety_stock = 50

    reorder_qty = max(
        0,
        forecast_demand + safety_stock - current_stock
    )

    return {
        "StockCode": request.StockCode,
        "PredictionDate": today.strftime("%Y-%m-%d"),
        "ForecastDemand": forecast_demand,
        "CurrentStock": current_stock,
        "SafetyStock": safety_stock,
        "SuggestedReorder": reorder_qty,
        "LastRevenue": round(float(latest["Revenue"]), 2),
        "LastOrderValue": round(float(latest["OrderValue"]), 2),
        "LastBasketSize": int(latest["BasketSize"])
    }