class Product:

    def __init__(self, sku, price):
        self.sku = sku
        self.price = price
        self.offers = []
    
    def add_offer(self, offer):
        self.offers.append(offer)


class Offer:

    def __init__(self, required_quantity, discount_price, free_sku=None):
        self.required_quantity = required_quantity
        self.discount_price = discount_price
        self.free_sku = free_sku
