''' Vegan grocieries shop'''
class Product:
    def __init__(self, name, quantity, buy_price, sell_price) -> None:
        self.name = name
        self.quantity = quantity
        self.sell_price = sell_price
        self.buy_price = buy_price

    def __repr__(self) -> str:
        return self.name
    
    def update_quantity(self, quantity):
        self.quantity += quantity
    
    def __dict__(self):
        return {self.name: [self.quantity, self.sell_price, self.buy_price]}
    
    def __getitem__(self, key):
        return self.__dict__()[key]
        

class Inventory:
    def __init__(self) -> None:
        self.inventory = {}
    
    def update_inventory(self, product):
        if product not in self.inventory:
            self.add_product(product)
        else:
            pass
    
    def add_product(self, product):
        self.inventory[str(product)] = product[product]

vegan_shop = Inventory()
apple = Product('apple', 10, 2, 1)
print(apple['apple'])
vegan_shop.update_inventory(apple)
vegan_shop.update_inventory(apple)