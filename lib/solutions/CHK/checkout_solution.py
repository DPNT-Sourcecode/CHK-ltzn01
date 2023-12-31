from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Set
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
        product_copy = copy.deepcopy(product)
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
    def __init__(self, item: Item, trigger_quantity: int):
        self.item = item
        self.trigger_quantity = trigger_quantity
        self.letter_affected = item.sku
        self.magnitude = self.calculate_magnitude()

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

    @abstractmethod
    def calculate_magnitude(self) -> float:
        """
        Method to calculate the magnitude of the discount
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
        self.bulk_price = bulk_price
        super().__init__(item, trigger_quantity)
        
    
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
    
    def calculate_magnitude(self) -> float:
        orginal_price = self.item.price * self.trigger_quantity
        discounted_price = self.bulk_price
        return orginal_price - discounted_price


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
        self.discounted_item = discounted_item
        super().__init__(item, trigger_quantity)
    
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
    
    def calculate_magnitude(self) -> float:
        """
        calculate the magnitude of the discount
        
        Returns:
            The magnitude of the discount
        """
        return self.discounted_item.price


class ComboDiscount(DiscountStrategy):
    """
    Discount strategy for buying a combination of items for a specific price
    """

    def __init__(self, items: List[Item], combo_price: float, trigger_quantity: int):
        """
        Initialise the combo discount.

        Args:
            items: A list of items that trigger the discount.
            combo_price: The price of the combo.
        """
        self.items = items
        self.combo_price = combo_price
        super().__init__(items[0], trigger_quantity)
        self.letters_affected = set(item.sku for item in items)

    def is_applicable(self, basket: Basket) -> bool:
        """
        Check if the combo discount is applicable.

        Args:
            basket: The basket to check for applicability.
        
        Returns:
            A boolean indicating whether the discount is applicable.
        """
        trigger_count = 0
        for product in basket.products:
            if product.sku in self.letters_affected and not product.discounted:
                trigger_count += 1
        return trigger_count >= self.trigger_quantity

    def apply_discount(self, basket: Basket) -> None:
        """
        Apply the combo discount.

        Args:
            basket: The basket to apply the discount to.
        """
        if not self.is_applicable(basket):
            return
        
        applicable_items = []
        for product in basket.products:
            if product.sku in self.letters_affected and not product.discounted:
                applicable_items.append(product)
        
        # Sort the items based on price in descending order for maximum effect
        applicable_items.sort(key=lambda x: x.price, reverse=True)

        for i in range(self.trigger_quantity):
            applicable_items[i].discounted_price = self.combo_price / self.trigger_quantity
            applicable_items[i].discounted = True
    
    def calculate_magnitude(self) -> float:
        """
        Calculate the magnitude of the discount.

        Returns:
            The magnitude of the discount.
        """
        orginal_price = sum(item.price for item in self.items)
        average_price = orginal_price / len(self.items)
        discount_per_item = average_price - (self.combo_price / self.trigger_quantity)
        return discount_per_item * self.trigger_quantity


####################################################################################################
############################################ analysis.py ###########################################
####################################################################################################


class Analysis(ABC):
    """
    Abstract base class for various analysis strategies
    """

    @abstractmethod
    def run(self, basket: Basket, discount_strategies: list[DiscountStrategy]) -> Basket:
        """
        Execute the analysis strategy.

        Args:
            basket: The basket to run the analysis on.
            discount_strategies: The list of discount strategies to apply to the basket.
        
        Returns:
            The basket after the analysis has been run
        """
        pass

class OptimisedAnalysis(Analysis):

    @staticmethod
    def apply_discounts(basket: Basket, discount_strategies_sorted: List[DiscountStrategy]) -> Basket:
        """
        Apply discount strategies to the basket.

        Args:
            basket: The basket of items.
            strategies_dict: A dictionary of discount strategies categorised by letters.
            basket_letters: A set of unique letters representing items in the basket.
        
        Returns:
            The basket after applying the discounts.
        """
        # Iterate through the discount strategies
        for discount_strategy in discount_strategies_sorted:
            # while the discount strategy is applicable, apply it to the basket
            while discount_strategy.is_applicable(basket):
                discount_strategy.apply_discount(basket)
        return basket

    def run(self, basket: Basket, discount_strategies: List[DiscountStrategy]) -> Basket:
        """
        Runs the analysis.

        Args:
            basket: The basket of items.
            discount_strategies: A list of discount strategies to apply to the basket.
        
        Returns:
            The basket after the analysis has been run.
        """
        # Take the discount strategies and sort them by magnitude, with the largest first
        discount_strategies_sorted = sorted(discount_strategies, key=lambda x: x.magnitude, reverse=True)
        basket = self.apply_discounts(basket, discount_strategies_sorted)
        return basket


####################################################################################################
############################################ checkout.py ###########################################
####################################################################################################

class CheckoutProcess:
    """
    Manages the checkout process.
    """
    def __init__(self, basket: Basket, analysis: Analysis, discount_strategies: List[DiscountStrategy] = None):
        """
        Initalise the checkout process.

        Args:
            basket: The basket to checkout.
            analysis: The analysis strategy to use.
            discount_strategies: The list of discount strategies to apply to the basket.
        """
        self.basket = basket
        self.analysis = analysis
        self.discount_strategies = discount_strategies or []

    def run_analysis(self):
        """
        Execute the analysis strategy.
        """
        self.basket = self.analysis.run(self.basket, self.discount_strategies)

    def total_price(self) -> float:
        """
        Return the total price of the basket
        """
        return sum(product.discounted_price for product in self.basket.products)

    def basket_summary(self):
        """
        Print a summary of the basket
        """
        for product in self.basket.products:
            print(product.sku, product.price, product.discounted_price)


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

    main_dict = {
        'A': Item('A', 50),
        'B': Item('B', 30),
        'C': Item('C', 20),
        'D': Item('D', 15),
        'E': Item('E', 40),
        'F': Item('F', 10),
        'G': Item('G', 20),
        'H': Item('H', 10),
        'I': Item('I', 35),
        'J': Item('J', 60),
        'K': Item('K', 70),
        'L': Item('L', 90),
        'M': Item('M', 15),
        'N': Item('N', 40),
        'O': Item('O', 10),
        'P': Item('P', 50),
        'Q': Item('Q', 30),
        'R': Item('R', 50),
        'S': Item('S', 20),
        'T': Item('T', 20),
        'U': Item('U', 40),
        'V': Item('V', 50),
        'W': Item('W', 20),
        'X': Item('X', 17),
        'Y': Item('Y', 20),
        'Z': Item('Z', 21)
    }


    # Initialise the basket
    basket = Basket()

    for sku in skus:
        if sku not in main_dict:
            return -1
        basket.add_product(main_dict[sku])

    discount_strategies = [
        BulkDiscount(main_dict['A'], 3, 130),
        BulkDiscount(main_dict['A'], 5, 200),
        BulkDiscount(main_dict['B'], 2, 45),
        FreeItemDiscount(main_dict['E'], 2, main_dict['B']),
        FreeItemDiscount(main_dict['F'], 2, main_dict['F']),
        BulkDiscount(main_dict['H'], 5, 45),
        BulkDiscount(main_dict['H'], 10, 80),
        BulkDiscount(main_dict['K'], 2, 120),
        FreeItemDiscount(main_dict['N'], 3, main_dict['M']),
        BulkDiscount(main_dict['P'], 5, 200),
        BulkDiscount(main_dict['Q'], 3, 80),
        FreeItemDiscount(main_dict['R'], 3, main_dict['Q']),
        FreeItemDiscount(main_dict['U'], 3, main_dict['U']),
        BulkDiscount(main_dict['V'], 2, 90),
        BulkDiscount(main_dict['V'], 3, 130),
        ComboDiscount([main_dict['S'], main_dict['T'], main_dict['X'], main_dict['Y'], main_dict['Z']], 45, 3)
    ]
    
 
    checkoutObject = CheckoutProcess(basket, OptimisedAnalysis(), discount_strategies)
    checkoutObject.run_analysis()

    print(int(round(checkoutObject.total_price(), 0)))

    return int(round(checkoutObject.total_price(), 0))

assert checkout('K') == 70
assert checkout('S') == 20
assert checkout('X') == 17