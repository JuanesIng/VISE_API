from decimal import Decimal
from pydantic import BaseModel
from app.models.enums import CardType

class Client(BaseModel):
    id: int
    name: str
    country: str
    monthly_income: float
    vise_club: bool
    card_type: CardType
