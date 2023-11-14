""" Vegan grocieries shop """
""" Be the change, go vegan """

import json
import os
from datetime import datetime
from products import Product
from commands import get_user_input, text_input


class Inventory:
    def __init__(self):
        self.inventory = {}
        self.gross_income = 0.0
        self.net_income = 0.0
        self.cost = 0.0

    # def __repr__(self) -> str:
    #     product_list = [
    #         f"{product.name}\t|\t{product.quantity}\t|\t{product.sell_price}"
    #         for product in sorted(self.inventory.values(), key=lambda x: x.name)
    #     ]
    #     return "\n".join(product_list)

    def __dict__(self) -> dict:
        sorted_inventory = sorted(self.inventory.values(), key=lambda x: x.name)
        return {
            item.name: [item.quantity, item.buy_price, item.sell_price]
            for item in sorted_inventory
        }

    def __list__(self) -> list:
        sorted_inventory = sorted(self.inventory.values(), key=lambda x: x.name)
        return [
            [item.name, item.quantity, f"{item.sell_price:.2f}"]
            for item in sorted_inventory
        ]

    def add_product(self, item: Product) -> None:
        self.inventory[item.name] = item

    def update_net_income(self, item, quantity: int) -> float:
        sold_product = self.inventory[item.name]
        earnings = (sold_product.sell_price - sold_product.buy_price) * quantity
        self.net_income += earnings
        return earnings

    def update_gross_income(self, item, quantity: int) -> float:
        sold_product = self.inventory[item.name]
        cost = sold_product.sell_price * quantity
        self.gross_income += cost
        return cost

    def update_inventory(self, item: Product) -> None:
        if item.name in self.inventory:
            self.update_quantity(item, item.quantity)
        else:
            self.add_product(item)

    def update_quantity(self, item: Product, quantity) -> None:
        if quantity < 0 and abs(quantity) > self.inventory[item.name].quantity:
            raise AssertionError(
                "Quantità superiore alla quantità in magazzino, operazione annuallata"
            )
        elif quantity < 0 and abs(quantity) == self.inventory[item.name].quantity:
            self.inventory.pop(item.name)
        else:
            self.inventory[item.name].quantity += quantity

    def sell_products(self, basket: list) -> None:
        for product in basket:
            for product_name, value in product.items():
                item = self.inventory[product_name]
                self.update_gross_income(item, value["quantity"])
                self.update_net_income(item, value["quantity"])
                self.update_quantity(item, -value["quantity"])

    def save_inventory(self) -> None:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        inventory_dict = {"last_save": now}
        inventory_dict["product format"] = {
            "name": ["quantity", "buy_price", "sell_price"]
        }
        inventory_dict["gross_income"] = self.gross_income
        inventory_dict["net_income"] = self.net_income
        inventory_dict["products"] = self.__dict__()
        with open("inventory.json", "w") as f:
            json.dump(inventory_dict, f, indent=4)

    def sell_shopping_cart(self) -> None:
        shopping_cart = []
        add_product = "si"
        exitFlag = False
        while add_product == "si":
            item_list = [list(item.keys())[0] for item in shopping_cart]
            input_name = text_input("Inserisci il nome del prodotto: ")
            while not self.product_exist(input_name):
                print("Prodotto terminato")
                input_name = text_input(
                    "Inserisci il nome del prodotto (fine per terminare):"
                )
                if input_name == "fine":
                    exitFlag = True
                    break
            if exitFlag:
                break
            if len(shopping_cart) == 0:
                input_quantity, exitFlag = self.get_user_quantity(input_name)
                if exitFlag:
                    break

                shopping_cart.append(
                    {
                        input_name: {
                            "quantity": input_quantity,
                            "partial": self.inventory[input_name].sell_price
                            * input_quantity,
                        }
                    }
                )
            else:
                if input_name in item_list:
                    pos = item_list.index(input_name)
                    # il prodotto è nel carrello
                    input_quantity, exitFlag = self.get_user_quantity(input_name)
                    if exitFlag:
                        break
                    shopping_cart[pos][input_name]["quantity"] += input_quantity
                    shopping_cart[pos][input_name]["partial"] += (
                        self.inventory[input_name].sell_price * input_quantity
                    )

                else:
                    # il prodotto non è nel carrello
                    input_quantity, exitFlag = self.get_user_quantity(input_name)
                    if exitFlag:
                        break
                    shopping_cart.append(
                        {
                            input_name: {
                                "quantity": input_quantity,
                                "partial": self.inventory[input_name].sell_price
                                * input_quantity,
                            }
                        }
                    )

            add_product = text_input("Aggiungere un altro prodotto? (si/NO): ")

        self.sell_products(shopping_cart)

        if len(shopping_cart) > 0:
            if any(
                quantity > 0
                for quantity in [
                    list(item.values())[0]["quantity"] for item in shopping_cart
                ]
            ):
                print("VENDITA REGISTRATA")
                basket_total = 0.0

                for product in shopping_cart:
                    basket_product = list(product.keys())[0]
                    basket_partial = product[basket_product]["partial"]
                    basket_total += basket_partial
                    basket_quantity = product[basket_product]["quantity"]
                    print(
                        f"{basket_quantity} X {basket_product}: €{basket_partial:.2f}"
                    )
                print(f"Totale: €{basket_total:.2f}")
                self.save_inventory()

    def add_to_inventory(self) -> None:
        product_name = text_input("Nome del prodotto: ")
        product_quantity = get_user_input("Quantità: ", int)

        if not self.product_exist(product_name):
            product_buy_price = float(get_user_input("Prezzo di acquisto: ", float))
            product_sell_price = float(get_user_input("Prezzo di vendita: ", float))
            product = Product(
                product_name,
                product_quantity,
                product_buy_price,
                product_sell_price,
            )

        else:
            product = Product(product_name, product_quantity)
        self.update_inventory(product)
        print(f"AGGIUNTO {product_quantity} X {product.name}")

    def product_exist(self, item_name: str) -> bool:
        return item_name in self.inventory

    def get_user_quantity(self, item_name: str) -> str:
        exitFlag = False
        input_quantity = get_user_input("Inserisci la quantità: ", int)
        while input_quantity > self.inventory[item_name].quantity:
            print(
                f"Quantità superiore a quella in magazzino {self.inventory[item_name].quantity}"
            )
            input_quantity = get_user_input("Inserisci la quantità: (0 annulla): ", int)
            if input_quantity == 0:
                exitFlag = True
                break
        return input_quantity, exitFlag


def load_inventory() -> Inventory:
    with open("inventory.json", "r") as f:
        inventory_dict = json.load(f)
    inventory = Inventory()
    for product, values in inventory_dict["products"].items():
        inventory.add_product(Product(product, values[0], values[1], values[2]))
    inventory.gross_income = inventory_dict["gross_income"]
    inventory.net_income = inventory_dict["net_income"]
    return inventory


if __name__ == "__main__":
    print("Module not executable")
