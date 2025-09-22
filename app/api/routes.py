from fastapi import APIRouter, HTTPException
from app.schemas.client import ClientCreate, ClientRegisterOK, ClientRegisterError
from app.schemas.purchase import PurchaseRequest, PurchaseOK, PurchaseError
from app.repositories.memory_client_repository import InMemoryClientRepository
from app.services.card_rules import CardRulesService
from app.services.purchase_service import PurchaseService

router = APIRouter()

# Inyección simple (en memoria)
client_repo = InMemoryClientRepository()
rules_service = CardRulesService()
purchase_service = PurchaseService(client_repo, rules_service)

@router.post("/client", response_model=ClientRegisterOK | ClientRegisterError, tags=["client"])
def register_client(body: ClientCreate):
    ok, message = rules_service.validate_client_eligibility(body)
    if not ok:
        return ClientRegisterError(status="Rejected", error=message)

    client = client_repo.create(body)
    return ClientRegisterOK(
        clientId=client.id,
        name=client.name,
        cardType=client.card_type.value,
        status="Registered",
        message=f"Cliente apto para tarjeta {client.card_type.value}"
    )

@router.post("/purchase", response_model=PurchaseOK | PurchaseError, tags=["purchase"])
def purchase(body: PurchaseRequest):
    client = client_repo.get_by_id(body.clientId)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    approved, result_or_error = purchase_service.process_purchase(client, body)
    if not approved:
        return PurchaseError(status="Rejected", error=result_or_error)

    return PurchaseOK(status="Approved", purchase=result_or_error)
