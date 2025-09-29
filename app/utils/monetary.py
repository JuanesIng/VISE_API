from decimal import Decimal, ROUND_HALF_UP

def money(x: float) -> float:
    # Redondeo estándar a 2 decimales
    return (x.quantize(float("0.01"), rounding=ROUND_HALF_UP))