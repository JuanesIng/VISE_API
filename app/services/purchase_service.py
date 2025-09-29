from decimal import Decimal
from datetime import datetime
from app.models.client import Client
from app.schemas.purchase import PurchaseRequest, PurchaseSummary
from app.repositories.client_repository import ClientRepository
from app.services.card_rules import CardRulesService
from app.utils.monetary import money

class PurchaseService:
    def __init__(self, repo: ClientRepository, rules: CardRulesService):
        self.repo = repo
        self.rules = rules

    def process_purchase(self, client: Client, req: PurchaseRequest):
        ok, err = self.rules.purchase_restriction(client.card_type, req.purchaseCountry, client.country)
        if not ok:
            return False, err

        dt: datetime = req.purchaseDate  # Pydantic ya lo parsea
        weekday = dt.weekday()           # 0=Lun ... 6=Dom
        is_foreign = (req.purchaseCountry != client.country)

        amount = float(str(req.amount))
        pct, label = self.rules.compute_benefit(
            card=client.card_type,
            amount=amount,
            weekday=weekday,
            is_foreign=is_foreign
        )

        discount = money(amount * pct)
        final_amt = money(amount - discount)

        summary = PurchaseSummary(
            clientId=client.id,
            originalAmount=money(amount),
            discountApplied=discount,
            finalAmount=final_amt,
            benefit=label
        )
        return True, summary