""" Vegan grocieries shop """
""" Be the change, go vegan """

import json
import os
from tabulate import tabulate
from datetime import datetime
from products import Product
from commands import get_number_input, get_text_input


class Inventory:
    def __init__(self):
        self.inventory = {}
        self.gross_income = 0.0
        self.net_income = 0.0
        self.cost = 0.0

    def __repr__(self) -> str:
        return tabulate(
            self.__list__(),
            headers=["PRODOTTO", "QUANTITA'", "PREZZO"],
            tablefmt="simple_outline",
        )

    def __dict__(self) -> dict:
        sorted_inventory = sorted(self.inventory.values(), key=lambda x: x.name)
        return {
            product.name: [product.quantity, product.buy_price, product.sell_price]
            for product in sorted_inventory
        }

    def __list__(self) -> list:
        sorted_inventory = sorted(self.inventory.values(), key=lambda x: x.name)
        return [
            [product.name, product.quantity, f"{product.sell_price:.2f}"]
            for product in sorted_inventory
        ]

    def add_product(self, product: Product) -> None:
        self.inventory[product.name] = product

    def update_net_income(self, product, quantity: int) -> float:
        sold_product = self.inventory[product.name]
        earnings = (sold_product.sell_price - sold_product.buy_price) * quantity
        self.net_income += earnings
        return earnings

    def update_gross_income(self, product, quantity: int) -> float:
        sold_product = self.inventory[product.name]
        cost = sold_product.sell_price * quantity
        self.gross_income += cost
        return cost

    def update_inventory(self, product: Product) -> None:
        if product.name in self.inventory:
            self.update_quantity(product, product.quantity)
        else:
            self.add_product(product)

    def update_quantity(self, product: Product, quantity) -> None:
        if quantity < 0 and abs(quantity) > self.inventory[product.name].quantity:
            raise ValueError(
                "Quantità superiore alla quantità in magazzino, operazione annuallata"
            )
        elif quantity < 0 and abs(quantity) == self.inventory[product.name].quantity:
            self.inventory.pop(product.name)
        else:
            self.inventory[product.name].quantity += quantity

    def sell_products(self, shopping_cart: list) -> None:
        for product in shopping_cart:
            for product_name, properties in product.items():
                product = self.inventory[product_name]
                self.update_gross_income(product, properties["quantity"])
                self.update_net_income(product, properties["quantity"])
                self.update_quantity(product, -properties["quantity"])

    def sell_shopping_cart(self) -> None:
        shopping_cart = []
        add_product = "si"
        exitFlag = False

        while add_product == "si":
            product_list = [list(product.keys())[0] for product in shopping_cart]
            input_name = get_text_input("Inserisci il nome del prodotto: ")

            while not self.product_exist(input_name):
                print("Prodotto terminato")
                input_name = get_text_input(
                    "Inserisci il nome del prodotto (fine per uscire):"
                )
                exitFlag = True if input_name == "fine" else False
                if exitFlag:
                    break
            if exitFlag:
                break

            if len(shopping_cart) == 0:
                # il carrello è vuoto
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
                # il carrello non è vuoto
                if input_name in product_list:
                    # il prodotto è nel carrello
                    pos = product_list.index(input_name)
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

            add_product = get_text_input("Aggiungere un altro prodotto? (si/NO): ")

        self.sell_products(shopping_cart)

        if len(shopping_cart) > 0 and any([list(product.values())[0]["quantity"]>0 for product in shopping_cart]):
            print("VENDITA REGISTRATA")

            shopping_cart_total = 0.0
            for product in shopping_cart:
                shopping_cart_product_name = list(product.keys())[0]
                shopping_cart_partial_price = product[shopping_cart_product_name]["partial"]
                shopping_cart_product_quantity = product[shopping_cart_product_name]["quantity"]
                shopping_cart_total += shopping_cart_partial_price
                print(
                    f"{shopping_cart_product_quantity} X {shopping_cart_product_name}: €{shopping_cart_partial_price:.2f}"
                )

            print(f"Totale: €{shopping_cart_total:.2f}")

    def add_to_inventory(self) -> None:
        product_name = get_text_input("Nome del prodotto: ")
        product_quantity = get_number_input("Quantità: ", int)

        if not self.product_exist(product_name):
            # il prodotto non esiste nell'inventario
            product_buy_price = get_number_input("Prezzo di acquisto: ", float)
            product_sell_price = get_number_input("Prezzo di vendita: ", float)
            product = Product(
                product_name,
                product_quantity,
                product_buy_price,
                product_sell_price,
            )

        else:
            # il prodotto esiste nell'inventario
            product = Product(product_name, product_quantity)
        self.update_inventory(product)
        print(f"AGGIUNTO {product_quantity} X {product.name}")

    def product_exist(self, product_name: str) -> bool:
        return product_name in self.inventory

    def get_user_quantity(self, product_name: str) -> str:
        input_quantity = get_number_input(
            "Inserisci la quantità: (0 per uscire): ", int
        )
        exitFlag = True if input_quantity == 0 else False
        while input_quantity > self.inventory[product_name].quantity:
            print(
                f"Quantità superiore a quella in magazzino {self.inventory[product_name].quantity}"
            )
            input_quantity = get_number_input(
                "Inserisci la quantità: (0 per uscire): ", int
            )
            exitFlag = True if input_quantity == 0 else False
            if exitFlag:
                break
        return input_quantity, exitFlag

    def save_inventory(self) -> None:
        try:
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

        except Exception as e:
            print("Impossibile salvare il file inventory.json")

    def load_inventory():
        try:
            with open("inventory.json", "r") as f:
                inventory_dict = json.load(f)
            inventory = Inventory()
            inventory.gross_income = float(inventory_dict["gross_income"])
            inventory.net_income = float(inventory_dict["net_income"])
            for product, properties in inventory_dict["products"].items():
                inventory.add_product(
                    Product(product, float(properties[0]), float(properties[1]), float(properties[2]))
                )
            return inventory

        except Exception:
            print("File inventory.json non valido, nuovo database creato")
            if os.path.exists("inventory.json"):
                os.rename("inventory.json", "inventory.json.bak")
            print("Il file originale è stato rinominato in inventory.json.bak")
            return Inventory()


if __name__ == "__main__":
    print("Module not executable")
