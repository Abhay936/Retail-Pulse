from database import collection
from fastapi import APIRouter

router = APIRouter(
    prefix="/data_load",
    tags=["Data Load"]
)

@router.get("/dashboard")
def dashboard():
    records = list(collection.find({}, {"_id": 0}).limit(100))
    return {"data": records}