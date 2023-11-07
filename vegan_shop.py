''' Vegan grocieries shop'''
class Product:
    def __init__(self, name, quantity, price) -> None:
        self.name = name
        self.quantity = quantity
        self.price = price

class Inventory:
    def __init__(self) -> None:
        self.products = []
    
    def update_product(self, product):
        pass

    def remove_product(self, product):
        pass
    
    def add_product(self, product):
        pass
