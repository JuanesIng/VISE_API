from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from app.models.enums import CardType

class ClientCreate(BaseModel):
    name: str = Field(..., examples=["Juanito Doue"])
    country: str = Field(..., examples=["FRANCIA"])
    monthlyIncome: float = Field(..., gt=0, examples=[1200])
    viseClub: bool = Field(..., examples=[True])
    cardType: CardType = Field(..., examples=[CardType.PLATINUM])

class ClientRegisterOK(BaseModel):
    clientId: int
    name: str
    cardType: str
    status: str
    message: str

class ClientRegisterError(BaseModel):
    status: str
    error: str

    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "status": "Rejected",
            "error": "El cliente no cumple con la suscripción VISE CLUB requerida para Platinum"
        }]
    })
