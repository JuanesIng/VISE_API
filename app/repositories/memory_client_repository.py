from typing import Optional, Dict
from decimal import Decimal
from app.repositories.client_repository import ClientRepository
from app.models.client import Client
from app.schemas.client import ClientCreate
from app.models.enums import CardType

class InMemoryClientRepository(ClientRepository):
    def __init__(self):
        self._db: Dict[int, Client] = {}
        self._seq = 1

    def create(self, data: ClientCreate) -> Client:
        client = Client(
            id=self._seq,
            name=data.name,
            country=data.country,
            monthly_income=Decimal(str(data.monthlyIncome)),
            vise_club=data.viseClub,
            card_type=CardType(data.cardType)
        )
        self._db[self._seq] = client
        self._seq += 1
        return client

    def get_by_id(self, client_id: int) -> Optional[Client]:
        return self._db.get(client_id)