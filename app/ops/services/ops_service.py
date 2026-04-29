def reserve_stock(product_id, quantity):
    """
    Mock OPS API call.
    Simulates stock reservation and store assignment.
    """
    return {
        "status": "reserved",
        "eta_minutes": 15,
        "store_id": "STORE-99"
    }

def confirm_stock_reduction(product_id, quantity):
    """
    Mock OPS API call.
    Confirmed after payment.
    """
    return True
