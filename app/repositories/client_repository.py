from abc import ABC, abstractmethod
from typing import Optional
from app.models.client import Client
from app.schemas.client import ClientCreate

class ClientRepository(ABC):
    @abstractmethod
    def create(self, data: ClientCreate) -> Client: ...
    @abstractmethod
    def get_by_id(self, client_id: int) -> Optional[Client]: ...