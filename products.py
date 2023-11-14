class Product:
    def __init__(
        self, name: str, quantity: int, buy_price: float = 0.0, sell_price: float = 0.0
    ):
        self.name = name
        self.quantity = quantity
        self.sell_price = float(sell_price)
        self.buy_price = float(buy_price)

    def __repr__(self) -> str:
        return self.name

    def __getitem__(self, item):
        return [self.quantity, self.buy_price, self.sell_price]
