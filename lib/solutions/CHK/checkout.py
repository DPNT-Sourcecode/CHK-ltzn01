from items import Item, Basket
from analysis import Analysis
from discounts import DiscountStrategy
from typing import List

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
