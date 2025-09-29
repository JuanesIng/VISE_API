from decimal import Decimal
from app.schemas.client import ClientCreate
from app.models.enums import CardType

BANNED_COUNTRIES = {"China", "Vietnam", "India", "Irán", "Iran"}  

class CardRulesService:
    # --- Restricciones de elegibilidad (registro) ---
    def validate_client_eligibility(self, data: ClientCreate) -> tuple[bool, str]:
        card = data.cardType
        income = float(str(data.monthlyIncome))
        club = data.viseClub
        country = data.country

        if card == CardType.CLASSIC:
            return True, "Classic sin restricciones"

        if card == CardType.GOLD:
            if income < float("500"):
                return False, "Ingreso mínimo de 500 USD requerido para Gold"
            return True, "Gold apto"

        if card == CardType.PLATINUM:
            if income < float("1000"):
                return False, "Ingreso mínimo de 1000 USD requerido para Platinum"
            if not club:
                return False, "Suscripción VISE CLUB requerida para Platinum"
            return True, "Platinum apto"

        if card in (CardType.BLACK, CardType.WHITE):
            if income < float("2000"):
                return False, f"Ingreso mínimo de 2000 USD requerido para {card.value}"
            if not club:
                return False, f"Suscripción VISE CLUB requerida para {card.value}"
            if country in BANNED_COUNTRIES:
                return False, f"Clientes residentes en {', '.join(sorted(BANNED_COUNTRIES))} no pueden solicitar {card.value}"
            return True, f"{card.value} apto"

        return False, "Tipo de tarjeta inválido"

    # --- Restricciones de compra (extra para Black/White) ---
    def purchase_restriction(self, card: CardType, purchase_country: str, client_country: str) -> tuple[bool, str | None]:
        if card in (CardType.BLACK, CardType.WHITE) and purchase_country in BANNED_COUNTRIES:
            return False, f"El cliente con tarjeta {card.value} no puede realizar compras desde {purchase_country}"
        return True, None

    # --- Beneficios ---
    def compute_benefit(self, *, card: CardType, amount: float, weekday: int, is_foreign: bool) -> tuple[float, str | None]:
        """
        Devuelve (porcentaje_descuento, etiqueta). No acumula; aplica el MAYOR válido.
        weekday: 0=Lunes ... 6=Domingo
        """
        pct = float("0")
        label = None

        def try_set(new_pct: str, new_label: str):
            nonlocal pct, label
            p = float(new_pct)
            if p > pct:
                pct = p
                label = new_label

        # Classic: sin beneficios
        if card == CardType.CLASSIC:
            return float("0"), None

        # Gold
        if card == CardType.GOLD:
            if weekday in (0, 1, 2) and amount > float("100"):
                try_set("0.15", "Lun-Mar-Mié - Descuento 15%")

        # Platinum
        if card == CardType.PLATINUM:
            if weekday in (0, 1, 2) and amount > float("100"):
                try_set("0.20", "Lun-Mar-Mié - Descuento 20%")
            if weekday == 5 and amount > float("200"):
                try_set("0.30", "Sábado - Descuento 30%")
            if is_foreign:
                try_set("0.05", "Compra en el exterior - 5%")

        # Black
        if card == CardType.BLACK:
            if weekday in (0, 1, 2) and amount > float("100"):
                try_set("0.25", "Lun-Mar-Mié - Descuento 25%")
            if weekday == 5 and amount > float("200"):
                try_set("0.35", "Sábado - Descuento 35%")
            if is_foreign:
                try_set("0.05", "Compra en el exterior - 5%")

        # White
        if card == CardType.WHITE:
            if weekday in (0, 1, 2, 3, 4) and amount > float("100"):
                try_set("0.25", "Lun-Vie - Descuento 25%")
            if weekday in (5, 6) and amount > float("200"):
                try_set("0.35", "Sáb-Dom - Descuento 35%")
            if is_foreign:
                try_set("0.05", "Compra en el exterior - 5%")

        return pct, label