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
    def categorise_discount_strategies(discount_strategies: List[DiscountStrategy]) -> Dict[str, List[DiscountStrategy]]:
        """
        Catergorise the discount strategies based in the items they affect.

        Args:
            discount_strategies: List of discount strategies.
        """
        strategies_dict = {}
        for strategy in sorted(discount_strategies, key=lambda x: x.trigger_quantity, reverse=True):
            letter = strategy.letter_affected
            if letter not in strategies_dict:
                strategies_dict[letter] = []
            strategies_dict[letter].append(strategy)
        return strategies_dict
    
    @staticmethod
    def get_basket_letters(basket: Basket) -> Set[str]:
        """
        Get a set of unique letters representing items in the basket.

        Args:
            basket: The basket of items.
        
        Returns:
            A set of unique letters
        """
        return {product.sku for product in basket.products}

    @staticmethod
    def apply_discounts(basket: Basket, strategies_dict: Dict[str, List[DiscountStrategy]], basket_letters: Set[str]) -> Basket:
        """
        Apply discount strategies to the basket.

        Args:
            basket: The basket of items.
            strategies_dict: A dictionary of discount strategies categorised by letters.
            basket_letters: A set of unique letters representing items in the basket.
        
        Returns:
            The basket after applying the discounts.
        """
        for letter in basket_letters:
            if letter in strategies_dict:
                for strategy in strategies_dict[letter]:
                    while strategy.is_applicable(basket):
                        strategy.apply_discount(basket)
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
        strategies_dict = self.categorise_discount_strategies(discount_strategies)
        basket.products.sort(key=lambda x: x.sku)
        basket_letters = self.get_basket_letters(basket)
        return self.apply_discounts(basket, strategies_dict, basket_letters)


####################################################################################################
############################################ checkout.py ###########################################
####################################################################################################

class Checkout:
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
        'K': Item('K', 80),
        'L': Item('L', 90),
        'M': Item('M', 15),
        'N': Item('N', 40),
        'O': Item('O', 10),
        'P': Item('P', 50),
        'Q': Item('Q', 30),
        'R': Item('R', 50),
        'S': Item('S', 30),
        'T': Item('T', 20),
        'U': Item('U', 40),
        'V': Item('V', 50),
        'W': Item('W', 20),
        'X': Item('X', 90),
        'Y': Item('Y', 10),
        'Z': Item('Z', 50)
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
        BulkDiscount(main_dict['K'], 2, 150),
        FreeItemDiscount(main_dict['N'], 3, main_dict['M']),
        BulkDiscount(main_dict['P'], 5, 200),
        BulkDiscount(main_dict['Q'], 3, 80),
        FreeItemDiscount(main_dict['R'], 3, main_dict['Q']),
        FreeItemDiscount(main_dict['U'], 3, main_dict['U']),
        BulkDiscount(main_dict['V'], 2, 90),
        BulkDiscount(main_dict['V'], 3, 130)
    ]
    
 
    checkout = Checkout(basket, OptimisedAnalysis(), discount_strategies)
    checkout.run_analysis()

    print(int(round(checkout.total_price(), 0)))

    return int(round(checkout.total_price(), 0))

# The below work
assert checkout('BEBEEE') == 160
assert checkout('LGCKAQXFOSKZGIWHNRNDITVBUUEOZXPYAVFDEPTBMQLYJRSMJCWH') == 1880
assert checkout('EEEEBB') == 160
assert checkout('BEBEEE') == 160