from collections import Counter

class Basket:

    def __init__(self):
        self.items = Counter()
        self.total = 0

    def add(self, product):
        self.items[product.sku] += 1
        self.total += product.price