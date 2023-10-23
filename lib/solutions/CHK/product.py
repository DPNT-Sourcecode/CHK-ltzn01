# Behaviour-Oriented Class
class Offer:

    def __init__(self, required_quantity, discount_price, free_sku=None):
        self.required_quantity = required_quantity
        self.discount_price = discount_price
        self.free_sku = free_sku

# Data-Oriented Class
class Product:
    """
    Represents a product in a supermarket.

    Attributes:
        sku (str): 
        price (float): The price of the product
        offers (list of Offer): A list of special offers applicable
    """

    def __init__(self, sku, price):
        """
        Initialises a new Product instance

        Args:
            sku (str): Unique ID for the Product
            price (float): The price of the product
        """
        self.sku = sku
        self.price = price
        self.offers = []
    
    def add_offer(self, offer: Offer) -> None:
        """
        Add a special offer to the product

        Args:
            offer (Offer): The special offer to be added to the product.
        """
        self.offers.append(offer)



