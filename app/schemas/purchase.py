from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class PurchaseRequest(BaseModel):
    clientId: int = Field(..., examples=[1])
    amount: Decimal = Field(..., gt=0, examples=[250])
    currency: str = Field(..., min_length=3, max_length=3, examples=["USD"])
    purchaseDate: datetime = Field(..., examples=["2025-09-20T14:30:00Z"])
    purchaseCountry: str = Field(..., examples=["Francia"])

class PurchaseSummary(BaseModel):
    clientId: int
    originalAmount: float
    discountApplied: float
    finalAmount: float
    benefit: str | None = None

class PurchaseOK(BaseModel):
    status: str
    purchase: PurchaseSummary

class PurchaseError(BaseModel):
    status: str
    error: str
