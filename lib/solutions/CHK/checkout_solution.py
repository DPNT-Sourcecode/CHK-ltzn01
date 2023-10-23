
def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.
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
    
    total = 0
    for item, count in counts.items():
        price = prices[item]


test_sku = "AAAB"
checkout(test_sku)

