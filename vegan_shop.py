""" Vegan grocieries shop """
""" Be the change, go vegan """

import json
import os
from datetime import datetime
from tabulate import tabulate


COMMANDS = {
    "aggiungi": "aggiungi un prodotto al magazzino",
    "elenca": "elenca i prodotto in magazzino",
    "vendi": "registra una vendita effettuata",
    "profitti": "mostra i profitti totali",
    "aiuto": "mostra i possibili comandi",
    "chiudi": "esci dal programma",
}


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


class Inventory:
    def __init__(self):
        self.inventory = {}
        self.gross_income = 0.0
        self.net_income = 0.0
        self.cost = 0.0

    def __repr__(self) -> str:
        product_list = "\n".join(
            [
                f"{product.name}\t|\t{product.quantity}\t|\t{product.sell_price}"
                for product in sorted(self.inventory.values(), key=lambda x: x.name)
            ]
        )
        return str(product_list)

    def __dict__(self) -> dict:
        sorted_inventory = sorted(self.inventory.values(), key=lambda x: x.name)
        return {
            item.name: [item.quantity, item.buy_price, item.sell_price]
            for item in sorted_inventory
        }

    def __list__(self) -> list:
        products = []
        for product_name, product in vegan_shop.inventory.items():
            products.append([product_name, product.quantity, product.sell_price])
        return products

    def update_net_income(self, product, quantity: int) -> float:
        sold_product = vegan_shop.inventory[product.name]
        earnings = sold_product.sell_price - sold_product.buy_price
        self.net_income += (earnings) * quantity
        return earnings

    def update_gross_income(self, product, quantity: int) -> float:
        sold_product = vegan_shop.inventory[product.name]
        cost = sold_product.sell_price * quantity
        self.gross_income += cost
        return cost

    def update_inventory(self, product: Product) -> None:
        if product.name in self.inventory:
            self.update_quantity(product, product.quantity)
        else:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        self.inventory[product.name] = product

    def sell_products(self, basket: list) -> None:
        # TODO, aggiorna quantità in modo corretto, rileggi le specifiche per capire cosa serve e ragiona sul flusso di cassa
        """
        aggiorna quantità
        aggiorna net_income
        """
        for item in basket:
            for product_name, values in item.items():
                product = self.inventory[product_name]
                self.update_gross_income(product, values["quantity"])
                self.update_net_income(product, values["quantity"])
                self.update_quantity(product, -values["quantity"])

    def update_quantity(self, product: Product, quantity) -> None:
        if abs(quantity) > self.inventory[product.name].quantity:
            raise AssertionError(
                "Quantità superiore alla quantità in magazzino, operazione annuallata"
            )
        if abs(quantity) == self.inventory[product.name].quantity and quantity < 0:
            self.inventory.pop(product.name)
        else:
            self.inventory[product.name].quantity += quantity

    def save_inventory(self) -> None:
        now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        inventory_dict = {"last_save": now}
        inventory_dict["product format"] = {
            "name": ["quantity", "buy_price", "sell_price"]
        }
        inventory_dict["gross_income"] = self.gross_income
        inventory_dict["net_income"] = self.net_income
        inventory_dict["products"] = self.__dict__()
        with open("inventory.json", "w") as f:
            json.dump(inventory_dict, f, indent=4)

    def product_exist(self, product_name: str) -> bool:
        if product_name in self.inventory:
            return True
        else:
            return False


def load_inventory():
    with open("inventory.json", "r") as f:
        inventory_dict = json.load(f)
    inventory = Inventory()
    for product, values in inventory_dict["products"].items():
        inventory.add_product(Product(product, values[0], values[1], values[2]))
    inventory.gross_income = inventory_dict["gross_income"]
    inventory.net_income = inventory_dict["net_income"]
    return inventory


def helper():
    print("I comandi disponibili sono i seguenti: ")
    for cmd, help in COMMANDS.items():
        print(f"{cmd}: {help}")


def get_user_input(message, data_type):
    while True:
        user_input = input(f"{message}")
        try:
            value = data_type(user_input)
            if value < 0:
                raise ValueError("Il valore deve essere maggiore di 0")
            else:
                return value
        except ValueError:
            if data_type == int:
                print("Quantità non valida, devi inserire un numero intero")
            elif data_type == float:
                print("Quantità non valida, devi inserire un numero decimale")


def get_user_quantity():
    input_quantity = get_user_input("Inserisci la quantità: ", int)
    while input_quantity > vegan_shop.inventory[input_name].quantity:
        print(
            f"Quantità superiore a quella in magazzino {vegan_shop.inventory[input_name].quantity}"
        )
        input_quantity = get_user_input(
            "Inserisci la quantità: (0 per annullare): ", int
        )
        if input_name == 0:
            exitFlag = True
            break
    return input_quantity, exitFlag


if __name__ == "__main__":
    vegan_shop = load_inventory() if os.path.exists("inventory.json") else Inventory()

    user_cmd = ""

    while user_cmd != "chiudi":
        user_cmd = input("\nInserisci un comando: ").lower().strip()
        try:
            match user_cmd:
                case "aggiungi":
                    product_name = (
                        input("Inserisci il nome del prodotto: ").lower().strip()
                    )
                    product_quantity = get_user_input("Inserisci la quantità: ", int)

                    if not vegan_shop.product_exist(product_name):
                        product_buy_price = float(
                            get_user_input("Inserisci il prezzo di acquisto: ", float)
                        )
                        product_sell_price = float(
                            get_user_input("Inserisci il prezzo di vendita: ", float)
                        )
                        product = Product(
                            product_name,
                            product_quantity,
                            product_buy_price,
                            product_sell_price,
                        )

                    else:
                        product = Product(product_name, product_quantity)
                    vegan_shop.update_inventory(product)

                case "elenca":
                    headers = ["PRODOTTO", "QUANTITA'", "PREZZO"]
                    print(
                        tabulate(
                            vegan_shop.__list__(),
                            headers=headers,
                            tablefmt="simple_outline",
                        )
                    )

                case "vendita":
                    basket = []
                    add_product = "si"
                    while add_product == "si":
                        item_list = [list(item.keys())[0] for item in basket]
                        input_name = (
                            input("Inserisci il nome del prodotto: ").lower().strip()
                        )
                        while not vegan_shop.product_exist(input_name):
                            print("Prodotto terminato")
                            input_name = (
                                input(
                                    "Inserisci il nome del prodotto: (fine per terminare)"
                                )
                                .lower()
                                .strip()
                            )
                            if input_name == "fine":
                                exitFlag = True
                                break
                        if exitFlag:
                            break
                        if len(basket) == 0:
                            input_quantity, exitFlag = get_user_quantity()
                            if exitFlag:
                                break

                            basket.append(
                                {
                                    input_name: {
                                        "quantity": input_quantity,
                                        "partial": vegan_shop.inventory[
                                            input_name
                                        ].sell_price
                                        * input_quantity,
                                    }
                                }
                            )
                        else:
                            if input_name in item_list:
                                pos = item_list.index(input_name)
                                # il prodotto è nel carrello
                                input_quantity, exitFlag = get_user_quantity()
                                if exitFlag:
                                    break
                                basket[pos][input_name]["quantity"] += input_quantity
                                basket[pos][input_name]["partial"] += (
                                    vegan_shop.inventory[input_name].sell_price
                                    * input_quantity
                                )

                            else:
                                # il prodotto non è nel carrello
                                input_quantity, exitFlag = get_user_quantity()
                                if exitFlag:
                                    break
                                basket.append(
                                    {
                                        input_name: {
                                            "quantity": input_quantity,
                                            "partial": vegan_shop.inventory[
                                                input_name
                                            ].sell_price
                                            * input_quantity,
                                        }
                                    }
                                )

                        add_product = (
                            input("Aggiungere un altro prodotto? (si/NO): ")
                            .lower()
                            .strip()
                        )

                    for product in basket:
                        vegan_shop.sell_products(basket)

                    print("VENDITA REGISTRATA")
                    basket_total = 0.0

                    for product in basket:
                        basket_product = list(product.keys())[0]
                        basket_partial = product[basket_product]["partial"]
                        basket_total += basket_partial
                        basket_quantity = product[basket_product]["quantity"]
                        print(
                            f"{basket_quantity} X {basket_product}: €{basket_partial}"
                        )
                    print(f"Totale: €{basket_total}")

                case "profitti":
                    print(
                        f"Profitto: lordo=€{vegan_shop.gross_income} netto=€{vegan_shop.net_income}"
                    )

                case "aiuto":
                    helper()

                case "chiudi":
                    vegan_shop.save_inventory()

                case _:
                    print("Comando non valido")
                    helper()

        except ValueError:
            print(
                "Il valore inserito non è valido, quantità, prezzo di acquisto e di vendita devono essere numeri"
            )
        except Exception as e:
            print(e)
