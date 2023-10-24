from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Set
import copy
from items import Item, Basket
from discounts import DiscountStrategy

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

