from product import Product, Offer



product_a = Product('A', 50)
product_b = Product('B', 30)

# Add Product A Details
offer_a1 = Offer(3, 130)
offer_a2 = Offer(5, 200)
product_a.add_offer(offer_a1)
product_a.add_offer(offer_a2)

offer_b = Offer(2, 45)


# Add Product B Details




def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.

    Args:
        skus (str): A string containing the SKUs of all the products in the basket.
    
    Returns:
        int: The total checkout value of the items. Returns -1 for any illegal input.
    """


    # if not all(c in {'A', 'B', 'C', 'D', 'E'} for c in skus):
    #     return -1
    
    # # Need to add multiple offers for single item
    # # Object Oriented Style?
    
    # prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    # offers = {'A': (3, 130), 'B': (2, 45)}

    # counts = {}
    # for item in skus:
    #     counts[item] = counts.get(item, 0) + 1
    
    # total = 0
    # for item, count in counts.items():
    #     price = prices[item]

    #     if item in offers:
    #         offer_quantity, offer_price = offers[item]
    #         offer_count = count // offer_quantity
    #         total += offer_count * offer_price
    #         count -= offer_count * offer_quantity
    #     total += count * price

    # return total


