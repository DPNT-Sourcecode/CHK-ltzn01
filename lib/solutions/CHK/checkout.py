from collections import Counter

class Basket:

    def __init__(self):
        self.items = Counter()
        self.total = 0

    def add(self, product):
        self.items[product.sku] += 1
        self.total += product.price

class Checkout:

    def __init__(self, products):
        self.products = products
    
    def calculate_total(self, skus):
        basket = Basket()
        for sku in skus:
            if sku not in self.products:
                return -1
            basket.add(self.products[sku])
    
    
                

