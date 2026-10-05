import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_valid_payout_calculation():
    payload = {
        "merchant_id": "MERCH_123",
        "transactions": [
            {"tx_id": "t1", "type": "PAYMENT", "amount": 100.00},
            {"tx_id": "t2", "type": "REFUND", "amount": 20.00},
            {"tx_id": "t3", "type": "DISPUTE", "amount": 30.00}
        ]
    }
    response = client.post("/api/payouts/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Math: 100 - 20 (refund) - 30 (dispute amount) - 15 (dispute fee) = 35
    assert data["net_payout"] == 35.0
    assert data["fees_charged"] == 15.0

def test_floating_point_precision():
    payload = {
        "merchant_id": "MERCH_456",
        "transactions": [
            {"tx_id": "t1", "type": "PAYMENT", "amount": 0.10},
            {"tx_id": "t2", "type": "PAYMENT", "amount": 0.20}
        ]
    }
    response = client.post("/api/payouts/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    # A standard Python float calculation will yield 0.30000000000000004
    # We strictly expect the exact monetary value of 0.30
    assert data["net_payout"] == 0.30

def test_negative_amount_rejected():
    payload = {
        "merchant_id": "MERCH_789",
        "transactions": [
            {"tx_id": "t1", "type": "PAYMENT", "amount": -50.00}
        ]
    }
    response = client.post("/api/payouts/calculate", json=payload)
    assert response.status_code == 400

def test_zero_amount_rejected():
    payload = {
        "merchant_id": "MERCH_789",
        "transactions": [
            {"tx_id": "t1", "type": "PAYMENT", "amount": 0.00}
        ]
    }
    response = client.post("/api/payouts/calculate", json=payload)
    assert response.status_code == 400

def test_empty_transactions_rejected():
    payload = {
        "merchant_id": "MERCH_999",
        "transactions": []
    }
    response = client.post("/api/payouts/calculate", json=payload)
    assert response.status_code == 400

def test_invalid_merchant_id():
    payload = {
        "merchant_id": "INVALID_123",
        "transactions": [
            {"tx_id": "t1", "type": "PAYMENT", "amount": 10.00}
        ]
    }
    response = client.post("/api/payouts/calculate", json=payload)
    assert response.status_code == 400

def test_invalid_transaction_type():
    payload = {
        "merchant_id": "MERCH_123",
        "transactions": [
            {"tx_id": "t1", "type": "UNKNOWN", "amount": 10.00}
        ]
    }
    response = client.post("/api/payouts/calculate", json=payload)
    # Pydantic natively returns 422 for schema validation failures
    assert response.status_code == 422
