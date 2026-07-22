from fastapi import FastAPI

from api.customer_seg import router as customer_router
from  api.churn_api import router as churn_router
from api.forcasting_api import router as forecast_router
from api.inventory_sugg import router as inventory_router

app = FastAPI(
    title="Retail Analytics API",
    version="1.0"
)

app.include_router(customer_router)
app.include_router(churn_router)
app.include_router(forecast_router)
app.include_router(inventory_router)

@app.get("/")
def home():
    return {
        "message": "Retail Analytics API Running"
    }