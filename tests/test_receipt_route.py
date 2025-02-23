import pytest
from fastapi.testclient import TestClient
from receipt_processor.main import app

mock_receipt = {
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
}

client = TestClient(app)

@pytest.fixture
def receipt_id() -> str:
    response = client.post('/receipts/process', json=mock_receipt)
    return response.json()['id']

def test_main():
    response = client.get('/')
    assert response.status_code == 200

def test_process_receipt():
    response = client.post('/receipts/process', json=mock_receipt)
    assert response.status_code == 200
    assert response.json()['id']

# receipt_id is a fixture that runs the post receipt first as a setup, so value is in memory
def test_get_receipt_points(receipt_id: str):
    response = client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 200
    assert response.json()['points'] == 109

def test_get_receipt_points_failure():
    response = client.get(f'/receipts/{23}/points')
    assert response.status_code == 404

def test_process_receipt_failure():
    response = client.post('/receipts/process', data={'fail_this': 'fail please'})
    assert response.status_code == 400

def test_process_receipt_future():
    mock_receipt["purchaseDate"] = "2027-03-20"
    response = client.post('/receipts/process', json=mock_receipt)
    assert response.status_code == 400

def test_process_receipt_invalid_time_pattern():
    mock_receipt["purchaseTime"] = "9:23"
    response = client.post('/receipts/process', json=mock_receipt)
    assert response.status_code == 400