from typing import List

from src.cart.app.api.model import ShoppingCartProduct


def calculate_total(products: List[ShoppingCartProduct]) -> float:
    total = 0
    for product in products:
        total += product.quantity * product.unit_price
    return total