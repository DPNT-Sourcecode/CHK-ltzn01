from basket import Basket

class Checkout:

    def __init__(self, products):
        self.products = products
    
    def calculate_total(self, skus):
        basket = Basket()
        for sku in skus:
            if sku not in self.products:
                return -1
            basket.add(self.products[sku])
