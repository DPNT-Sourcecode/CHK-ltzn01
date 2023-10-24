from dataclasses import dataclass, field
from typing import List, Optional
import copy
# File imports are not working for Accelerate Runner
# All code will have to be on this single file

# from items import Item, Basket

####################################################################################################
############################################### items.py ###########################################
####################################################################################################


@dataclass
class Item:
    """
    Represents an item in a shopping basket.

    Attributes:
        sku: The item's SKU.
        price: The item's price.
        discounted_price: The Item's discounted price
        discounted: A boolean indicating whether the item has been discounted.
    """
    sku: str
    price: float
    discounted_price: Optional[float] = None
    discounted: bool = False

    def __post_init__(self):
        """
        Post-initialisation to set discounted price to the orginal price if not provided.
        """
        if self.discounted_price is None:
            self.discounted_price = self.price


@dataclass
class Basket:
    """
    A class representing a shopping basket.

    Attributes:
        products: a list of products in the basket.
    """
    products: List[Item] = field(default_factory=list)

    def add_product(self, product: Item):
        """
        Add a product to the basket.

        Args:
            product: The product to add to the basket
        """
        product_copy = copy.copy(product)
        self.products.append(product_copy)
    
    def remove_product(self, product: Item):
        """
        Remove a product from the basket.

        Args:
            product: The product to remove from the basket.
        """
        self.products.remove(product)
    
    def view_products(self):
        """
        Print details of all products in the basket
        """
        for product in self.products:
            print(product.sku, product.price)


    


def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.

    Args:
        skus (str): A string containing the SKUs of all the products in the basket.
    
    Returns:
        int: The total checkout value of the items. Returns -1 for any illegal input.
    """
    item_a = Item('A', 50)
    print(item_a)

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
print(checkout("A"))



