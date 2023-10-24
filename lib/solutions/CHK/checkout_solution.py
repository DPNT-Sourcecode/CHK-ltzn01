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
            # If the product is already in the basket, we don't want to add it again
            # but we do want to update the price. It must not have been discounted before.
            for product in basket.products:
                if product.sku == self.discounted_item.sku and not product.discounted:
                    product.discounted_price = 0
                    product.discounted = True
                    break
            # If the Product is not in the basket, we want to add it
            self.discounted_item.discounted_price = 0
            self.discounted_item.discounted = True
            basket.add_product(self.discounted_item)


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
    # Define the Products
    item_a = Item('A', 50)
    item_b = Item('B', 30)
    item_c = Item('C', 20)
    item_d = Item('D', 15)
    item_e = Item('E', 40)
    item_f = Item('F', 10)
    item_g = Item('G', 20)
    item_h = Item('H', 10)
    item_i = Item('I', 35)
    item_j = Item('J', 60)
    item_k = Item('K', 80)
    item_l = Item('L', 90)
    item_m = Item('M', 15)
    item_n = Item('N', 40)
    item_o = Item('O', 10)
    item_p = Item('P', 50)
    item_q = Item('Q', 30)
    item_r = Item('R', 50)
    item_s = Item('S', 30)
    item_t = Item('T', 20)
    item_u = Item('U', 40)
    item_v = Item('V', 50)
    item_w = Item('W', 20)
    item_x = Item('X', 90)
    item_y = Item('Y', 10)
    item_z = Item('Z', 50)


    # Initialise the basket
    basket = Basket()

    # Get Products from string
    for letter in skus:
        if letter == item_a.sku:
            basket.add_product(item_a)
        elif letter == item_b.sku:
            basket.add_product(item_b)
        elif letter == item_c.sku:
            basket.add_product(item_c)
        elif letter == item_d.sku:
            basket.add_product(item_d)
        elif letter == item_e.sku:
            basket.add_product(item_e)
        elif letter == item_f.sku:
            basket.add_product(item_f)
        elif letter == item_g.sku:
            basket.add_product(item_g)
        elif letter == item_h.sku:
            basket.add_product(item_h)
        elif letter == item_i.sku:
            basket.add_product(item_i)
        elif letter == item_j.sku:
            basket.add_product(item_j)
        elif letter == item_k.sku:
            basket.add_product(item_k)
        elif letter == item_l.sku:
            basket.add_product(item_l)
        elif letter == item_m.sku:
            basket.add_product(item_m)
        elif letter == item_n.sku:
            basket.add_product(item_n)
        elif letter == item_o.sku:
            basket.add_product(item_o)
        elif letter == item_p.sku:
            basket.add_product(item_p)
        elif letter == item_q.sku:
            basket.add_product(item_q)
        elif letter == item_r.sku:
            basket.add_product(item_r)
        elif letter == item_s.sku:
            basket.add_product(item_s)
        elif letter == item_t.sku:
            basket.add_product(item_t)
        elif letter == item_u.sku:
            basket.add_product(item_u)
        elif letter == item_v.sku:
            basket.add_product(item_v)
        elif letter == item_w.sku:
            basket.add_product(item_w)
        elif letter == item_x.sku:
            basket.add_product(item_x)
        elif letter == item_y.sku:
            basket.add_product(item_y)
        elif letter == item_z.sku:
            basket.add_product(item_z)
        else:
            return -1
    
    # Define Discount Strategies
    a_discount_1 = BulkDiscount(item_a, 3, 130)
    a_discount_2 = BulkDiscount(item_a, 5, 200)
    b_discount_1 = BulkDiscount(item_b, 2, 45)
    e_discount_1 = FreeItemDiscount(item_e, 2, item_b)
    f_discount_1 = FreeItemDiscount(item_f, 2, item_f)
    h_discount_1 = BulkDiscount(item_h, 5, 45)
    h_discount_2 = BulkDiscount(item_h, 10, 80)
    k_discount_1 = BulkDiscount(item_k, 2, 150)
    n_discount_1 = BulkDiscount(item_n, 3, 120)
    p_discount_1 = BulkDiscount(item_p, 5, 200)
    q_discount_1 = BulkDiscount(item_q, 3, 80)
    r_discount_1 = FreeItemDiscount(item_r, 3, item_q)
    u_discount_1 = FreeItemDiscount(item_u, 3, item_u)
    v_discount_1 = BulkDiscount(item_v, 2, 90)
    v_discount_2 = BulkDiscount(item_v, 3, 130)

    checkout = Checkout(basket, BruteForceAnalysis(), [a_discount_1, a_discount_2, b_discount_1, e_discount_1, 
                                                       f_discount_1, h_discount_1, h_discount_2, k_discount_1, 
                                                       n_discount_1, p_discount_1, q_discount_1, r_discount_1, 
                                                       u_discount_1, v_discount_1, v_discount_2])
    checkout.run_analysis()

    return int(round(checkout.total_price(), 0))


assert checkout("VVV") == 130

