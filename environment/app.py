from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import List

app = FastAPI()

class Transaction(BaseModel):
    tx_id: str
    type: str  # "PAYMENT", "REFUND", "DISPUTE"
    amount: float

    @validator("type")
    def validate_type(cls, v):
        if v not in ("PAYMENT", "REFUND", "DISPUTE"):
            raise ValueError("Invalid transaction type")
        return v

class PayoutRequest(BaseModel):
    merchant_id: str
    transactions: List[Transaction]

def calculate_payout(transactions: List[Transaction]) -> dict:
    total_payout = 0.0
    fee_total = 0.0
    
    for tx in transactions:
        if tx.type == "PAYMENT":
            total_payout += tx.amount
        elif tx.type == "REFUND":
            total_payout -= tx.amount
        elif tx.type == "DISPUTE":
            total_payout -= tx.amount
            total_payout -= 15.00
            fee_total += 15.00
            
    return {
        "net_payout": total_payout,
        "fees_charged": fee_total
    }

@app.post("/api/payouts/calculate")
def calculate_merchant_payout(payload: PayoutRequest):
    result = calculate_payout(payload.transactions)
    return result
