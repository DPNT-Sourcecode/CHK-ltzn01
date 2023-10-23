from product import Product, Offer
from checkout import Checkout
from basket import Basket


# Define the products
product_a = Product('A', 50)
product_b = Product('B', 30)
product_c = Product('C', 20)
product_d = Product('D', 15)
product_e = Product('E', 40)

# Add Product A Details
offer_a1 = Offer(3, 130)
offer_a2 = Offer(5, 200)
product_a.add_offer(offer_a1)
product_a.add_offer(offer_a2)

# Add Product B Details
offer_b1 = Offer(2, 45)
product_b.add_offer(offer_b1)


# Define all products to checkout
products = {product_a.sku: product_a, product_b.sku: product_b}

# Checkout
Checkout = Checkout(products)




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
