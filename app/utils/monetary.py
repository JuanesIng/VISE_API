from decimal import Decimal, ROUND_HALF_UP

def money(x: Decimal) -> Decimal:
    # Redondeo estándar a 2 decimales
    return (x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))