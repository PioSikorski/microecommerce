def calculate_total(cart) -> float:
    total = 0
    for product in cart.products:
        total += product.quantity * product.unit_price
    return total