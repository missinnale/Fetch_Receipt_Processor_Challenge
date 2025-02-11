from fastapi import APIRouter, status, HTTPException
from receipt_processor.internal import point_processor
import uuid
import hashlib

router = APIRouter(
    tags=["receipts"],
    responses={
        200: {'description': 'everything is fine, no seriously'},
        201: {'description': 'you created that'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'}
    }
)

# this would be replaced by an actual db, caching, etc.
session_store: dict = {}

@router.post('/receipts/process', status_code=status.HTTP_201_CREATED)
def process_receipt(receipt: dict):
    receipt_id = str(uuid.UUID(hashlib.md5((receipt['retailer'] + receipt['purchaseDate'] + receipt['purchaseTime']).encode('UTF-8')).hexdigest()))
    points = point_processor.get_receipt_points(receipt)
    session_store[receipt_id] = {'receipt': receipt, 'total_points': points}
    return {"id": receipt_id}

@router.get('/receipts/{id}/points')
def get_receipt_points(id: str):
    if id not in session_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Receipt ID could not be found.')
    receipt = session_store[id]
    return {"points": receipt['total_points']}
