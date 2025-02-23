from datetime import date
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from receipt_processor.internal import point_processor
from receipt_processor.models.receipt import Receipt
import uuid
import hashlib

class ReceiptIDOut(BaseModel):
    id: str

class PointsOut(BaseModel):
    points: int

router = APIRouter(
    tags=["receipts"]
)

# this would be replaced by an actual db, caching, etc.
session_store: dict = {}

# would prefer status code to be 201 created, but matching schema provided
@router.post('/receipts/process', status_code=status.HTTP_200_OK,
        description="Submits a receipt for processing.",
        response_description="Returns the ID assigned to the receipt.",
        response_model=ReceiptIDOut,
        responses={400: {"description": "The receipt is invalid."}}
    )
def process_receipt(receipt: Receipt):
    if receipt.purchase_date > date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The receipt is invalid. It contains a future date.")
    receipt_id = str(uuid.UUID(hashlib.md5((receipt.retailer + str(receipt.purchase_date) + receipt.purchase_time).encode('UTF-8')).hexdigest()))
    points = point_processor.get_receipt_points(receipt)
    session_store[receipt_id] = {'receipt': receipt, 'total_points': points}
    return {"id": receipt_id}

@router.get('/receipts/{id}/points',
        description="Returns the points awarded for the receipt.",
        response_description="The number of points awarded.",
        response_model=PointsOut,
        responses={404: {"description": "No receipt found for that ID."}}
    )
def get_receipt_points(id: str):
    if id not in session_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No receipt found for that ID.")
    receipt = session_store[id]
    return {"points": receipt['total_points']}
