from enum import Enum

class CardType(str, Enum):
    CLASSIC = "Classic"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    BLACK = "Black"
    WHITE = "White"