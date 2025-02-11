from urllib import response
import pytest
from fastapi.testclient import TestClient
from receipt_processor.main import app

mock_receipt = '''{
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        }
    ],
    "total": "9.00"
    }'''

# post example date to process endpoint, check if id is returned in specified format

# set up for get request, hit points endpoint with specific id, check correct points are calculated

client = TestClient(app)

@pytest.fixture
def receipt_id() -> str:
    response = client.post('/receipts/process', content=mock_receipt)
    return response.json()['id']

def test_main():
    response = client.get('/')
    assert response.status_code == 200

def test_process_receipt():
    response = client.post('/receipts/process', content=mock_receipt)
    assert response.status_code == 201
    assert response.json()['id']

# receipt_id is a fixture that runs the post receipt first as a setup
def test_get_receipt_points(receipt_id: str):
    response = client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 200
    assert response.json()['points'] == 109

def test_get_receipt_points_failure():
    response = client.get(f'/receipts/{23}/points')
    assert response.status_code == 404

def test_process_receipt_failure():
    response = client.post('/receipts/process', content='fail this')
    assert response.status_code == 400
