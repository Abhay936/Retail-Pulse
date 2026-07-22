# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import pandas as pd
# import joblib
# from datetime import timedelta
# import pandas as pd
# import pandas as pd
# from backend.database import collection

# def load_data():
#     cursor = collection.find({}, {"_id": 0})
#     return pd.DataFrame(list(cursor))

# router = APIRouter(
#     prefix="/customer-segmentation",
#     tags=["Customer Segmentation"]
# )

# # ======================================================
# # Load Dataset
# # ======================================================
# # @st.cache_data(ttl=600)
# # def load_data():
# #     records = list(collection.find())
# #     df = pd.DataFrame(records)
# #     if "_id" in df.columns:
# #         df.drop(columns="_id", inplace=True)
# #     return df


# df = load_data()

# df.dropna(subset=["Customer ID"], inplace=True)

# df["Customer ID"] = df["Customer ID"].astype(int)

# df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# df["TotalPrice"] = df["Quantity"] * df["Price"]

# snapshot_date = df["InvoiceDate"].max() + timedelta(days=1)

# # ======================================================
# # Load Models
# # ======================================================

# scaler = joblib.load("backend/models/customer_scaler.pkl")

# kmeans = joblib.load("backend/models/customer_segmentation.pkl")

# # ======================================================
# # Request Schema
# # ======================================================

# class CustomerRequest(BaseModel):
#     customer_id: int

# # ======================================================
# # RFM Calculation Function
# # ======================================================

# def calculate_rfm(customer_id: int):

#     customer = df[df["Customer ID"] == customer_id]

#     if customer.empty:
#         raise HTTPException(
#             status_code=404,
#             detail="Customer ID not found."
#         )

#     recency = (
#         snapshot_date -
#         customer["InvoiceDate"].max()
#     ).days

#     frequency = customer["Invoice"].nunique()

#     monetary = round(customer["OrderValue"].sum(), 2)

#     return {
#         "Customer ID": customer_id,
#         "Recency": recency,
#         "Frequency": frequency,
#         "Monetary": monetary
#     }

# # ======================================================
# # RFM API
# # ======================================================

# @router.post("/rfm")
# def get_rfm(request: CustomerRequest):

#     return calculate_rfm(request.customer_id)

# # ======================================================
# # Customer Segmentation API
# # ======================================================

# @router.post("/predict")
# def predict_customer_segment(request: CustomerRequest):

#     rfm = calculate_rfm(request.customer_id)

#     rfm_df = pd.DataFrame([{
#         "Recency": rfm["Recency"],
#         "Frequency": rfm["Frequency"],
#         "Monetary": rfm["Monetary"]
#     }])

#     rfm_scaled = scaler.transform(rfm_df)

#     cluster = int(kmeans.predict(rfm_scaled)[0])

#     # Change these names according to your training notebook
#     segment_mapping = {
#     0: "At Risk",
#     1: "Champions",
#     2: "Loyal Customers",
#     3: "Potential Loyalists"
# }

#     segment = segment_mapping.get(cluster, "Unknown")

#     return {
#         "Customer ID": rfm["Customer ID"],
#         "Recency": rfm["Recency"],
#         "Frequency": rfm["Frequency"],
#         "Monetary": rfm["Monetary"],
#         "Cluster": cluster,
#         "Segment": segment
#     }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from datetime import timedelta
from database import collection

router = APIRouter(
    prefix="/customer-segmentation",
    tags=["Customer Segmentation"]
)

# ======================================================
# Load Models
# ======================================================

scaler = joblib.load("models/customer_scaler.pkl")
kmeans = joblib.load("models/customer_segmentation.pkl")

# ======================================================
# Snapshot Date (Load Once)
# ======================================================

latest = list(collection.aggregate([
    {
        "$addFields": {
            "InvoiceDateObj": {
                "$dateFromString": {
                    "dateString": "$InvoiceDate"
                }
            }
        }
    },
    {
        "$group": {
            "_id": None,
            "max_date": {
                "$max": "$InvoiceDateObj"
            }
        }
    }
]))

if not latest:
    raise Exception("Dataset is empty.")

SNAPSHOT_DATE = (
    pd.to_datetime(latest[0]["max_date"])
    + timedelta(days=1)
)

# ======================================================
# Request Schema
# ======================================================

class CustomerRequest(BaseModel):
    customer_id: int

# ======================================================
# RFM Calculation
# ======================================================

def calculate_rfm(customer_id: int):

    pipeline = [
    {
        "$match": {
            "Customer ID": int(customer_id)
        }
    },
    {
        "$addFields": {
            "InvoiceDateObj": {
                "$dateFromString": {
                    "dateString": "$InvoiceDate"
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$Customer ID",
            "LastPurchase": {
                "$max": "$InvoiceDateObj"
            },
            "Invoices": {
                "$addToSet": "$Invoice"
            },
            "Monetary": {
                "$sum": "$OrderValue"
            }
        }
    }
]

    result = list(collection.aggregate(pipeline))

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Customer ID not found."
        )

    customer = result[0]

    recency = (
        SNAPSHOT_DATE -
        pd.to_datetime(customer["LastPurchase"])
    ).days

    frequency = len(customer["Invoices"])

    monetary = round(customer["Monetary"], 2)

    return {
        "Customer ID": customer_id,
        "Recency": recency,
        "Frequency": frequency,
        "Monetary": monetary
    }

# ======================================================
# RFM API
# ======================================================

@router.post("/rfm")
def get_rfm(request: CustomerRequest):
    return calculate_rfm(request.customer_id)


# ======================================================
# Customer Segmentation API
# ======================================================

@router.post("/predict")
def predict_customer_segment(request: CustomerRequest):

    # Calculate RFM
    rfm = calculate_rfm(request.customer_id)

    # Prepare DataFrame
    rfm_df = pd.DataFrame([{
        "Recency": rfm["Recency"],
        "Frequency": rfm["Frequency"],
        "Monetary": rfm["Monetary"]
    }])

    # Scale Features
    rfm_scaled = scaler.transform(rfm_df)

    # Predict Cluster
    cluster = int(kmeans.predict(rfm_scaled)[0])

    # Segment Names
    segment_mapping = {
        0: "At Risk",
        1: "Champions",
        2: "Loyal Customers",
        3: "Potential Loyalists"
    }

    segment = segment_mapping.get(cluster, "Unknown")

    return {
        "Customer ID": rfm["Customer ID"],
        "Recency": int(rfm["Recency"]),
        "Frequency": int(rfm["Frequency"]),
        "Monetary": float(rfm["Monetary"]),
        "Cluster": cluster,
        "Segment": segment
    }