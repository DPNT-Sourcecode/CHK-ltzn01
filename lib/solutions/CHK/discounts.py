from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Set
import copy
from items import Item, Basket


class DiscountStrategy(ABC):
    """
    Abstract base class for various discount strategies

    Attributes:
        item: The item that the discount applies to.
        trigger_quantity: The quantity of items required to trigger the discount.
        bulk_price: The price of the item when the discount is triggered
    """
    def __init__(self, item: Item, trigger_quantity: int):
        self.item = item
        self.trigger_quantity = trigger_quantity
        self.letter_affected = item.sku

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
        super().__init__(item, trigger_quantity)
        self.bulk_price = bulk_price
        self.letter_affected = item.sku
    
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
        item: The item that triggers the discount.
        trigger_quantity: The quantity of trigger items required to trigger the discount.
        discounted_item: THe item that is discounted.
    """

    def __init__(self, item: Item, trigger_quantity: int, discounted_item: Item):
        """
        Initialise the free item discount.

        Args:
            item: The item that triggers the discount.
            trigger_quantity: The quantity of trigger items required to trigger the discount.
            discounted_item: The item that is discounted.
        """
        super().__init__(item, trigger_quantity)
        self.discounted_item = discounted_item
    
    def is_applicable(self, basket: Basket) -> bool:
        """
        Check if the free item discount is applicable.

        Args:
            basket: The basket to check for applicability
        """
        trigger_count = 0
        for product in basket.products:
            if product.sku == self.item.sku and not product.discounted:
                trigger_count += 1
        return trigger_count >= self.trigger_quantity
    
    def apply_discount(self, basket: Basket) -> None:
        if self.is_applicable(basket):
            trigger_count = 0
            for product in basket.products:
                if product.sku == self.item.sku and not product.discounted:
                    product.discounted = True
                    trigger_count += 1
                    if trigger_count == self.trigger_quantity:
                        break

            # Try to find and discount an existing product in the basket
            for product in basket.products:
                if product.sku == self.discounted_item.sku and not product.discounted:
                    product.discounted_price = 0
                    product.discounted = True
                    return

            # If the product is not in the basket or all instances are already discounted, add a new discounted item
            discounted_item_copy = copy.deepcopy(self.discounted_item)
            discounted_item_copy.discounted_price = 0
            discounted_item_copy.discounted = True
            basket.add_product(discounted_item_copy)

