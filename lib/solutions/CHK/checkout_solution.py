
def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.

    Args:
        skus (str): A string containing the SKUs of all the products in the basket.
    
    Returns:
        int: The total checkout value of the items. Returns -1 for any illegal input.
    """
    # First validated the input
    if not all(c in {'A', 'B', 'C', 'D'} for c in skus):
        return -1
    
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    offers = {'A': (3, 130), 'B': (2, 45)}

    # Calculate number of each item 
    counts = {}
    for item in skus:
        counts[item] = counts.get(item, 0) + 1
    
    # Calculate total cost for each item
    total = 0
    for item, count in counts.items():
        price = prices[item]
        total += count * price
        # Figure out way for offers
        if item in offers:
            offer_quantity, offer_price = offers[item]
            offer_count = count // offer_quantity
            total += offer_count * offer_price
            count -= offer_count * offer_quantity
    return total


test_sku = "AAAB"
print(checkout(test_sku))



