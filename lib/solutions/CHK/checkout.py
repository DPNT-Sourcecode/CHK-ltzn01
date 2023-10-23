from collections import Counter
from product import Product

# Data-Oriented Class
class Basket:
    """
    A class representing a shopping basket.

    Attributes:
        items (Counter): A counter of the products in the basket
        total (float): The total price of the products in the basket.
    """

    def __init__(self):
        """Initialises a new empty basket."""
        self.items = Counter()
        self.total = 0

    def add(self, product: Product) -> None:
        """
        Add a product to a basket.

        Args:
            product (Product): The product to be added.
        """
        self.items[product.sku] += 1
        self.total += product.price

# Behavior-Oriented Class - think about splitting up
class Checkout:
    """
    A class repesenting the checkout process
    """

    def __init__(self, products):
        """
        Initialises a new checkout with the given products.

        Args:
            products (dict of str: Product): A dictionary of products available.
        """
        self.products = products
    
    @staticmethod
    def discount_value(offer):
        return -offer.discount_value()
    
    def calculate_total(self, skus: str) -> int:
        """
        Calculate the total price of the products in the basket

        Args:
            skus (str): A string of SKUs representing the products in the basket.
        
            Returns:
                Int: The total price of the products in the basket. Returns -1 for any illegal input.
        """         
        basket = Basket()
        for sku in skus:
            if sku not in self.products:
                return -1
            basket.add(self.products[sku])
        
        for sku, count in basket.items.items():
            product = self.products[sku]
            for offer in sorted(product.offers, key=self.discount_value):
                count = self.apply_offer(basket, product, offer, count)
        
        return int(basket.total)
    
    def apply_offer(self, basket, product, offer, count):
        """
        Applies a special offer to the products in the basket.

        Args:
            basket (Basket): The shopping basket.
            product (Product): The product the offer applies to.
            offer (Offer): The special offer.
            count (int): the quantity of the product in the basket.
        
        Returns:
            int: The remaining count of the product after applying offer
        """
        if offer.free_sku:
            # Leave this out for now - not implemented
            pass
        # else:
        #     offer_count = count // offer.required_quantity


    

                



