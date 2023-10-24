from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Optional
import copy

# File imports are not working for Accelerate Runner
# All code will have to be on this single file

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


####################################################################################################
########################################### discounts.py ###########################################
####################################################################################################

class DiscountStrategy(ABC):
    """
    Abstract base class for various discount strategies

    Attributes:
        item: The item that the discount applies to.
        trigger_quantity: The quantity of items required to trigger the discount.
        bulk_price: The price of the item when the discount is triggered
    """

    @abstractmethod
    def is_applicable(self, basket: 'Basket') -> bool:
        """
        Method to check if the discount can be applied to the basket
        """
        pass

    @abstractmethod
    def apply_discount(self, basket: 'Basket') -> None:
        """
        Method to apply the discount to the basket
        """
        pass

class BulkDiscount(DiscountStrategy):
    """
    Applies a bulk discount based on specific quantity

    Attributes:
        item: The item that the discount applies to.
        trigger_quantity: The quantity of items required to trigger the discount.
        Bulk_price: The price of the item when the discount is triggered.
    """

    def __init__(self, item: Item, trigger_quantity: int, bulk_price: float):
        self.item = item
        self.trigger_quantity = trigger_quantity
        self.bulk_price = bulk_price
    
    def is_applicable(self, basket: Basket) -> bool:
        """
        Check if the bulk purchase discount is applicable.

        Args:
            basket: The basket to check for applicability.
        
        Returns:
            A boolean indicating whether the discount is applicable
        """
        trigger_count = 0
        for product in basket.products:
            if product.sku == self.item.sku and not product.discounted:
                trigger_count += 1
        return trigger_count >= self.trigger_quantity
    
    def apply_discount(self, basket: Basket) -> None:
        """
        Apply the bulk purchase discount.

        Args:
            basket: The basket to apply the discount to
        """
        num_changed = 0
        if self.is_applicable(basket):
            for product in basket.products:
                if product.sku == self.item.sku and not product.discounted and num_changed < self.trigger_quantity:
                    product.discounted_price = self.bulk_price / self.trigger_quantity
                    product.discounted = True
                    num_changed += 1


class FreeItemDiscount(DiscountStrategy):
    """
    Discount strategy for applying a buy x get y free discount.

    Attributes:
        trigger_item: The item that triggers the discount.
        trigger_quantity: The quantity of trigger items required to trigger the discount.
        discounted_item: THe item that is discounted.
    """

    def __init__(self, trigger_item: Item, trigger_quantity: int, discounted_item: Item):
        """
        Initialise the free item discount.

        Args:
            trigger_item: The item that triggers the discount.
            trigger_quantity: The quantity of trigger items required to trigger the discount.
            discounted_item: The item that is discounted.
        """
        self.trigger_item = trigger_item
        self.trigger_quantity = trigger_quantity
        self.discounted_item = discounted_item
    
    def is_applicable(self, basket: Basket) -> bool:
        """
        Check if the free item discount is applicable.

        Args:
            basket: The basket to check for applicability
        """
        trigger_count = 0
        for product in basket.products:
            if product.sku == self.trigger_item.sku and not product.discounted:
                trigger_count += 1
        return trigger_count >= self.trigger_quantity
    
    def apply_discount(self, basket: Basket) -> None:
        if self.is_applicable(basket):
            trigger_count = 0
            for product in basket.products:
                if product.sku == self.trigger_item.sku and not product.discounted:
                    product.discounted = True
                    trigger_count += 1
                    if trigger_count == self.trigger_quantity:
                        break
            # If the product is already in the basket, we don't want to add it again
            # but we do want to update the price. It must not have been discounted before.
            for product


####################################################################################################
######################################## checkout_solution.py ######################################
####################################################################################################


def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.

    Args:
        skus (str): A string containing the SKUs of all the products in the basket.
    
    Returns:
        int: The total checkout value of the items. Returns -1 for any illegal input.
    """
    # Define the Products
    item_a = Item('A', 50)
    item_b = Item('B', 30)
    item_c = Item('C', 20)
    item_d = Item('D', 15)
    item_e = Item('E', 40)

    # Initialise the basket
    basket = Basket()



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



