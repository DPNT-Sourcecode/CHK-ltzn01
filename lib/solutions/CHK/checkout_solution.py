
def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.

    Args:
        skus (str): A string containing the SKUs of all the products in the basket.
    
    Returns:
        int: The total checkout value of the items. Returns -1 for any illegal input.
    """
    pass

    # # Think about putting these into some sort of JSON format?
    # # Define the products
    # product_a = Product('A', 50)
    # product_b = Product('B', 30)
    # product_c = Product('C', 20)
    # product_d = Product('D', 15)
    # product_e = Product('E', 40)

    # # Add Product A Offers
    # offer_a1 = Offer(3, 130)
    # offer_a2 = Offer(5, 200)
    # product_a.add_offer(offer_a1)
    # product_a.add_offer(offer_a2)

    # # Add Product B Offers
    # offer_b1 = Offer(2, 45)
    # product_b.add_offer(offer_b1)

    # # Add Product E Offers
    # offer_e = Offer(2, 0, free_sku='B')
    # product_e.add_offer(offer_e)


    # # Define all products to checkout
    # products = {"A": product_a, 
    #             "B": product_b,
    #             "C": product_c,
    #             "D": product_d,
    #             "E": product_e
    # }

    # # Checkout
    # checkout_instance = Checkout(products)

    # total = checkout_instance.calculate_total(skus)

    # return total

# assert checkout("A") == 50
# assert checkout("AAA") == 130
# assert checkout("EEB") == 80
# assert checkout("BEE") == 80



