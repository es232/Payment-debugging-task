#!/bin/bash
# Oracle solution that successfully fixes the bugs

cd "$(dirname "$0")/.."

# Safely overwrite app.py with the correct, debugged implementation
cat << 'EOF' > environment/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
from decimal import Decimal

app = FastAPI()

class Transaction(BaseModel):
    tx_id: str
    type: str  # "PAYMENT", "REFUND", "DISPUTE"
    amount: Decimal

    @validator("type")
    def validate_type(cls, v):
        if v not in ("PAYMENT", "REFUND", "DISPUTE"):
            raise ValueError("Invalid transaction type")
        return v

class PayoutRequest(BaseModel):
    merchant_id: str
    transactions: List[Transaction]

def calculate_payout(transactions: List[Transaction]) -> dict:
    total_payout = Decimal("0.0")
    fee_total = Decimal("0.0")
    
    for tx in transactions:
        if tx.type == "PAYMENT":
            total_payout += tx.amount
        elif tx.type == "REFUND":
            total_payout -= tx.amount
        elif tx.type == "DISPUTE":
            total_payout -= tx.amount
            total_payout -= Decimal("15.00")
            fee_total += Decimal("15.00")
            
    return {
        "net_payout": float(round(total_payout, 2)),
        "fees_charged": float(round(fee_total, 2))
    }

@app.post("/api/payouts/calculate")
def calculate_merchant_payout(payload: PayoutRequest):
    if not payload.merchant_id.startswith("MERCH_"):
        raise HTTPException(status_code=400, detail="Invalid merchant_id format")
        
    if not payload.transactions:
        raise HTTPException(status_code=400, detail="Transactions list cannot be empty")
        
    for tx in payload.transactions:
        if tx.amount <= 0:
            raise HTTPException(status_code=400, detail="Transaction amounts must be strictly positive")
            
    result = calculate_payout(payload.transactions)
    return result
EOF

echo "Oracle solution applied successfully."
