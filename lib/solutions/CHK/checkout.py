from collections import Counter
from product import Product

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

class Checkout:

    def __init__(self, products):
        self.products = products
    
    def calculate_total(self, skus):
        basket = Basket()
        for sku in skus:
            if sku not in self.products:
                return -1
            basket.add(self.products[sku])
    
    def apply_offer(self, basket, product, offer, count):

    

                

