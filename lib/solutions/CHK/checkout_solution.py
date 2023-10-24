from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Set
import copy
from items import Item, Basket
from discounts import DiscountStrategy, BulkDiscount, FreeItemDiscount
from checkout import CheckoutProcess
from analysis import Analysis, OptimisedAnalysis

def create_items():
    return {
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


def checkout(skus: str) -> int:
    """
    Calculate total price of a number of items.

    Args:
        skus (str): A string containing the SKUs of all the products in the basket.
    
    Returns:
        int: The total checkout value of the items. Returns -1 for any illegal input.
    """

    main_dict = create_items()
    fresh_main_dict = {sku: copy.deepcopy(item) for sku, item in main_dict.items()}


    # Initialise the basket
    basket = Basket()

    for sku in skus:
        if sku not in fresh_main_dict:
            return -1
        basket.add_product(fresh_main_dict[sku])

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
    
 
    checkoutObject = CheckoutProcess(basket, OptimisedAnalysis(), discount_strategies)
    checkoutObject.run_analysis()

    print(int(round(checkoutObject.total_price(), 0)))

    return int(round(checkoutObject.total_price(), 0))



